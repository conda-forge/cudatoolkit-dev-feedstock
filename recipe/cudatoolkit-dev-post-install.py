#!/usr/bin/env python3
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
import platform
import urllib.parse as urlparse
from pathlib import Path
from contextlib import contextmanager
from tempfile import TemporaryDirectory as tempdir
from distutils.dir_util import copy_tree


class Extractor(object):
    """Extractor base class, platform specific extractors should inherit
    from this class.
    """

    def __init__(self, cudatoolkit_config):
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
        self.cu_blob = cudatoolkit_config["blob"]
        self.conda_prefix = os.environ.get("CONDA_PREFIX")
        self.prefix = os.environ["PREFIX"]
        self.src_dir = Path(self.conda_prefix) / "pkgs" / "cuda-toolkit"
        self.blob_dir = Path(self.conda_prefix) / "pkgs" / self.cu_name
        os.makedirs(self.blob_dir, exist_ok=True)

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

    def copy_files(self, source, destination, ignore=None):
        dest = Path(destination)
        if dest.exists() and dest.is_dir():
            shutil.rmtree(dest, ignore_errors=True)
        elif dest.exists() and dest.is_file():
            dest.unlink()
        else:
            shutil.copytree(
                source, destination, symlinks=True, ignore=ignore, ignore_dangling_symlinks=True)


class LinuxExtractor(Extractor):
    """The Linux Extractor
    """

    def extract(self):
        print("Extracting on Linux")
        runfile = self.blob_dir / self.cu_blob
        os.chmod(runfile, 0o777)

        with tempdir() as tmpdir:
            cmd = [
                str(runfile),
                "--silent",
                "--toolkit",
                f"--toolkitpath={tmpdir}",
                "--override"
            ]
            subprocess.run(cmd, env=os.environ.copy(), check=True)
            toolkitpath = tmpdir

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
                    'Something went wrong in executing `{}`: directory `{}` does not exist'
                    .format(' '.join(cmd), toolkitpath))

            self.copy_files(toolkitpath, self.src_dir)
        os.remove(runfile)


class WinExtractor(Extractor):
    """The Windows extractor
    """

    def download(self, url, target_full_path):
        cmd = ["curl", url, "-o", target_full_path]
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as exc:
            raise exc

    def extract(self):
        print("Extracting on Windows")
        runfile = self.blob_dir / self.cu_blob
                
        with tempdir() as tmpdir:
            cmd = [
                "7za",
                "x",
                str(runfile), 
                f"-o{tmpdir}"
            ] 
            subprocess.run(cmd, env=os.environ.copy(), check=True)
            toolkitpath = tmpdir

            if not os.path.isdir(toolkitpath):
                print('STATUS:',status)
                os.system('dir %s' % (tmpdir))
                raise RuntimeError(
                    'Something went wrong in executing `{}`: directory `{}` does not exist'
                    .format(' '.join(cmd), toolkitpath))

			# Install files directly to the library prefix. 
			# This is because Windows 10 requires either admin privileges or developer mode enabled (since Creators Update) for the creation of symlinks.
			# These options are not guaranteed at the user end
            target_dir = os.path.join(self.prefix, "Library")
            # ignore=shutil.ignore_patterns('*.nvi') 
            for toolkitpathroot, subdirs, files in os.walk(toolkitpath):
                for file in files:
                    src_file = os.path.join(toolkitpathroot, file)
                    os.chmod(src_file, 0o777)
                    if file == "cudadevrt.lib":
                        target_bin = os.path.join(target_dir, 'bin')
                        os.makedirs(target_bin, exist_ok=True)
                        shutil.copy2(src_file, target_bin)
                for subdir in subdirs:
                    if subdir in ['bin','include','lib','extras', 'libdevice']:
                        src = os.path.join(toolkitpathroot, subdir)
                        dst = os.path.join(target_dir, 'bin') if subdir=="libdevice" else os.path.join(target_dir, subdir)
                        if subdir=="lib" and platform.architecture()[0]=="64bit" and os.path.exists(os.path.join(src, 'x64')):
                            src = os.path.join(src, 'x64')
                        elif subdir=="lib" and platform.architecture()[0]=="32bit" and os.path.exists(os.path.join(src, 'Win32')):
                            src = os.path.join(src, 'win32')
                        else:
                            pass
                        # self.copy_files(src, dst, ignore=ignore)
                        copy_tree(src, dst)
        os.remove(runfile)

@contextmanager
def _hdiutil_mount(mntpnt, image):
    subprocess.check_call(["hdiutil", "attach", "-mountpoint", mntpnt, image])
    yield mntpnt
    subprocess.check_call(["hdiutil", "detach", mntpnt])


def check_platform():
    plt = sys.platform
    if plt.startswith("linux") or plt.startswith("win"):
        return
    else:
        raise RuntimeError("Unsupported platform: %s" % (plt))


def set_config():
    """Set necessary configurations"""

    cudatoolkit = {}
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
    url_prod_ext = f'compute/cuda/{cudatoolkit["version"]}/'
    cudatoolkit["base_url"] = urlparse.urljoin(url_dev, url_prod_ext)
    cudatoolkit["md5_url"] = urlparse.urljoin(
        url_dev_download, url_prod_ext + "docs/sidebar/md5sum.txt"
    )

    cudatoolkit["installers_url_ext"] = f"local_installers/"
    cudatoolkit["patch_url_ext"] = f""

    if sys.platform.startswith("win"):
        cudatoolkit["blob"] = f'cuda_{cudatoolkit["version"]}_{cudatoolkit["driver_version"]}_win10.exe'
    else:
        cudatoolkit["blob"] = f'cuda_{cudatoolkit["version"]}_{cudatoolkit["driver_version"]}_linux.run'

    return cudatoolkit


def _main():

    print("Running Post installation")

    os.environ['DISPLAY'] = ''
    
    cudatoolkit_config = set_config()

    # get an extractor
    check_platform()
    extractor = WinExtractor(cudatoolkit_config) if sys.platform.startswith("win") else LinuxExtractor(cudatoolkit_config)

    # download binaries
    extractor.download_blobs()

    # Extract
    extractor.extract()


if __name__ == "__main__":
    _main()
