"""
Adapted from https://github.com/numba/conda-recipe-cudatoolkit

BSD 2-Clause License

Copyright (c) 2018 Onwards, Quansight, LLC
Copyright (c) 2017, Continuum Analytics, Inc.

All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. """

import glob
import json
import os
import shutil
import subprocess
import sys
import urllib.parse as urlparse
from pathlib import Path
from contextlib import contextmanager
from tempfile import TemporaryDirectory as tempdir


class Extractor(object):
    """Extractor base class, platform specific extractors should inherit
    from this class.
    """

    def __init__(self, cudatoolkit_config, platform_config):
        """Initialise an instance:
        Arguments:
          cudatoolkit_config: the configuration for CUDA
          platform_config - the configuration for this platform
        """
        self.cu_name = cudatoolkit_config["name"]
        self.cu_version = cudatoolkit_config["release"]
        self.md5_url = cudatoolkit_config["md5_url"]
        self.base_url = cudatoolkit_config["base_url"]
        self.patch_url_text = cudatoolkit_config["patch_url_ext"]
        self.installers_url_ext = cudatoolkit_config["installers_url_ext"]
        self.cu_blob = platform_config["blob"]
        self.conda_prefix = os.environ.get("CONDA_PREFIX")
        self.prefix = os.environ["PREFIX"]
        self.src_dir = Path(self.conda_prefix) / "pkgs" / "cuda-toolkit"
        self.blob_dir = Path(self.conda_prefix) / "pkgs" / self.cu_name
        os.makedirs(self.blob_dir, exist_ok=True)

        self.symlinks = getplatform() == "linux"

    def create_activate_and_deactivate_scripts(self):
        activate_dir_path = Path(self.conda_prefix) / "etc" / "conda" / "activate.d"
        deactivate_dir_path = Path(self.conda_prefix) / "etc" / "conda" / "deactivate.d"

        os.makedirs(activate_dir_path, exist_ok=True)
        os.makedirs(deactivate_dir_path, exist_ok=True)

        # Copy cudatoolkit-dev-activate and cudatoolkit-dev-deactivate
        # to activate.d and deactivate.d directories

        scripts_dir = Path(self.prefix) / "scripts"
        activate_scripts_dir = scripts_dir / "activate.d"
        deactivate_scripts_dir = scripts_dir / "deactivate.d"

        activate_scripts_list = ["cudatoolkit-dev-activate.sh"]
        for file_name in activate_scripts_list:
            file_full_path = activate_scripts_dir / file_name
            shutil.copy(file_full_path, activate_dir_path)

        deactivate_scripts_list = ["cudatoolkit-dev-deactivate.sh"]

        for file_name in deactivate_scripts_list:
            file_full_path = deactivate_scripts_dir / file_name
            shutil.copy(file_full_path, deactivate_dir_path)

    def download(self, url, target_full_path):
        cmd = ["wget", url, "-O", target_full_path, "-q"]
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as exc:
            raise exc

    def download_blobs(self):
        """Downloads the binary blobs to the $BLOB_DIR
        """
        dl_url = urlparse.urljoin(self.base_url, self.installers_url_ext)
        dl_url = urlparse.urljoin(dl_url, self.cu_blob)
        dl_path = os.path.join(self.blob_dir, self.cu_blob)

        if os.path.isfile(dl_path):
            print("re-using previously downloaded %s" % (dl_path))
        else:
            print("downloading %s to %s" % (dl_url, dl_path))
        self.download(dl_url, dl_path)

    def extract(self, *args):
        """The method to extract files from the cuda binary blobs.
        Platform specific extractors must implement.
        """
        raise NotImplementedError("%s.extract(..)" % (type(self).__name__))

    def copy_files(self, source, destination):
        shutil.copytree(
            source, destination, symlinks=True, ignore_dangling_symlinks=True, dirs_exist_ok=True
        )


class LinuxExtractor(Extractor):
    """The Linux Extractor
    """

    def extract(self):
        print("Extracting on Linux")
        runfile = self.blob_dir / self.cu_blob
        os.chmod(runfile, 0o777)

        with tempdir() as tmpdir:
            cmd = [str(runfile),
                   f"--extract={tmpdir}",
                   #f"--defaultroot={tmpdir}",
                   "--override"]
            status = subprocess.run(cmd, check=True)
            toolkitpath = os.path.join(tmpdir, "cuda-toolkit")
            if not os.path.isdir(toolkitpath):
                installer = (glob.glob(os.path.join(tmpdir, 'cuda-linux*.run')) or [None])[0]
                if installer is not None:
                    print('Try using', installer)
                    subprocess.run(
                        [installer,
                         '-prefix=%s' % (toolkitpath),
                         '-noprompt'  # Implies acceptance of the EULA
                        ],
                        check=True
                    )
            if not os.path.isdir(toolkitpath):
                print('STATUS:',status)
                for fn in glob.glob('/tmp/cuda_install_*.log'):
                    f = open(fn, 'r')
                    print('-'*100, fn)
                    print(f.read())
                    print('-'*100)
                    f.close()
                os.system('ldd --version')
                os.system('ls -la %s' % (tmpdir))
                raise RuntimeError(
                    'Something went wrong in executing `{}`: directory `{}` does not exists'
                    .format(' '.join(cmd), toolkitpath))
            self.copy_files(toolkitpath, self.src_dir)
        os.remove(runfile)


class OsxExtractor(Extractor):
    """The osx Extractor
    """

    def _mount_extract(self, image, store):
        """Mounts and extracts the files from an image into store
        """
        mntpnt = str(self.blob_dir / "tmpstore")
        os.makedirs(mntpnt, exist_ok=True)
        subprocess.check_call(["hdiutil", "attach", "-mountpoint", mntpnt, image])
        cmd = " ".join(
            [
                "find",
                mntpnt,
                "-name",
                '"*.tar.gz"',
                "-exec",
                "tar",
                "xvf",
                "{}",
                f"--directory={store}",
                "';'",
            ]
        )

        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        subprocess.check_call(["hdiutil", "detach", mntpnt])

        shutil.rmtree(mntpnt, ignore_errors=True)

    def extract(self):
        runfile = self.blob_dir / self.cu_blob
        store = str(self.blob_dir / "store")
        os.makedirs(store, exist_ok=True)
        self._mount_extract(runfile, store)
        toolkitpath = (
            Path(store) / "Developer" / "NVIDIA" / "CUDA-{}".format(self.cu_version)
        )
        self.copy_files(toolkitpath, self.src_dir)
        os.remove(runfile)

        shutil.rmtree(store, ignore_errors=True)


@contextmanager
def _hdiutil_mount(mntpnt, image):
    subprocess.check_call(["hdiutil", "attach", "-mountpoint", mntpnt, image])
    yield mntpnt
    subprocess.check_call(["hdiutil", "detach", mntpnt])


def getplatform():
    plt = sys.platform
    if plt.startswith("linux"):
        return "linux"
    elif plt.startswith("darwin"):
        return "osx"
    else:
        raise RuntimeError("Unsupported platform: %s" % (plt))


def set_config():
    """Set necessary configurations"""

    cudatoolkit = {"linux": {}, "osx": {}}
    prefix = Path(os.environ["PREFIX"])
    extra_args = dict()
    with open(prefix / "bin" / "cudatoolkit-dev-extra-args.json", "r") as f:
        extra_args = json.loads(f.read())

    cudatoolkit["version"] = os.environ["PKG_VERSION"]
    cudatoolkit["name"] = os.environ["PKG_NAME"]
    cudatoolkit["buildnum"] = os.environ["PKG_BUILDNUM"]
    cudatoolkit["version_build"] = extra_args["version_build"]
    cudatoolkit["driver_version"] = extra_args["driver_version"]
    cudatoolkit["release"] = extra_args["release"]

    url_dev = os.environ.get(
        "PROXY_DEV_NVIDIA", "https://developer.download.nvidia.com/"
    )
    url_dev_download = os.environ.get(
        "PROXY_DEV_DOWNLOAD_NVIDIA", "http://developer.download.nvidia.com/"
    )
    url_prod_ext = f'compute/cuda/{cudatoolkit["release"]}/Prod/'
    cudatoolkit["base_url"] = urlparse.urljoin(url_dev, url_prod_ext)
    cudatoolkit["md5_url"] = urlparse.urljoin(
        url_dev_download, url_prod_ext + "docs/sidebar/md5sum.txt"
    )

    cudatoolkit["installers_url_ext"] = f"local_installers/"
    cudatoolkit["patch_url_ext"] = f""

    cudatoolkit["linux"] = {
        "blob": f'cuda_{cudatoolkit["version"]}_{cudatoolkit["driver_version"]}_rhel6.run'
    }

    cudatoolkit["osx"] = {"blob": f'cuda_{cudatoolkit["version"]}_mac.dmg'}

    return cudatoolkit


dispatcher = {"linux": LinuxExtractor, "osx": OsxExtractor}


def _main():

    print("Running Post installation")

    os.environ['DISPLAY'] = ''

    cudatoolkit_config = set_config()

    # get an extractor
    plat = getplatform()
    extractor_impl = dispatcher[plat]
    extractor = extractor_impl(cudatoolkit_config, cudatoolkit_config[plat])

    # create activate and deactivate scripts
    extractor.create_activate_and_deactivate_scripts()

    # download binaries
    extractor.download_blobs()

    # Extract
    extractor.extract()


if __name__ == "__main__":
    _main()
