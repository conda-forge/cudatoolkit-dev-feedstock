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

from __future__ import print_function

import json
import os
import shutil
import subprocess
import sys
import urllib.parse as urlparse
from pathlib import Path

from conda.exports import download, hashsum_file


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
        self.cu_version = cudatoolkit_config["version"]
        self.md5_url = cudatoolkit_config["md5_url"]
        self.base_url = cudatoolkit_config["base_url"]
        self.patch_url_text = cudatoolkit_config["patch_url_ext"]
        self.installers_url_ext = cudatoolkit_config["installers_url_ext"]
        self.cu_blob = platform_config["blob"]
        self.conda_prefix = os.environ.get("CONDA_PREFIX")
        self.prefix = os.environ["PREFIX"]
        self.src_dir = Path(self.conda_prefix) / "pkgs" / self.cu_name
        os.makedirs(self.src_dir, exist_ok=True)

        self.symlinks = getplatform() == "linux"
        self.debug_install_path = os.environ.get("DEBUG_INSTALLER_PATH")

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

        activate_scripts_list = [
            "cudatoolkit-dev-activate.sh",
            "cudatoolkit-dev-activate.bat",
        ]
        for file_name in activate_scripts_list:
            file_full_path = activate_scripts_dir / file_name
            shutil.copy(file_full_path, activate_dir_path)

        deactivate_scripts_list = [
            "cudatoolkit-dev-deactivate.sh",
            "cudatoolkit-dev-deactivate.bat",
        ]

        for file_name in deactivate_scripts_list:
            file_full_path = deactivate_scripts_dir / file_name
            shutil.copy(file_full_path, deactivate_dir_path)

    def download_blobs(self):
        """Downloads the binary blobs to the $SRC_DIR
        """
        dl_url = urlparse.urljoin(self.base_url, self.installers_url_ext)
        dl_url = urlparse.urljoin(dl_url, self.cu_blob)
        dl_path = os.path.join(self.src_dir, self.cu_blob)
        if not self.debug_install_path:
            print("downloading %s to %s" % (dl_url, dl_path))
            download(dl_url, dl_path)

        else:
            existing_file = os.path.join(self.debug_install_path, self.cu_blob)
            print("DEBUG: copying %s to %s" % (existing_file, dl_path))
            shutil.copy(existing_file, dl_path)

    def check_md5(self):
        """Checks the md5sums of the downloaded binaries
        """
        md5file = self.md5_url.split("/")[-1]
        path = os.path.join(self.src_dir, md5file)
        download(self.md5_url, path)

        # compute hash of blob
        blob_path = os.path.join(self.src_dir, self.cu_blob)
        md5sum = hashsum_file(blob_path, "md5")

        # get checksums
        with open(path, "r") as f:
            checksums = [x.strip().split() for x in f.read().splitlines() if x]

        # check md5 and filename match up
        check_dict = {x[0]: x[1] for x in checksums}
        assert check_dict[md5sum].startswith(self.cu_blob[:-7])

    def extract(self, *args):
        """The method to extract files from the cuda binary blobs.
        Platform specific extractors must implement.
        """
        raise RuntimeError("Must implement")

    def cleanup(self):
        """The method to delete unnecessary files after
        the installation process.
        """
        raise RuntimeError("Must implement")


class LinuxExtractor(Extractor):
    """The Linux Extractor
    """

    def extract(self):
        print("Extracting on Linux")
        runfile = os.path.join(self.src_dir, self.cu_blob)
        os.chmod(runfile, 0o777)
        cmd = [
            runfile,
            "--silent",
            "--toolkit",
            "--toolkitpath",
            str(self.src_dir),
            "--override",
        ]
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            print(
                "ERROR: Couldn't install Cudatoolkit: \
                   {reason}".format(
                    reason=e
                )
            )

    def cleanup(self):
        blob_path = os.path.join(self.src_dir, self.cu_blob)
        if os.path.exists(blob_path):
            os.remove(blob_path)

        else:
            pass


class OsxExtractor(Extractor):
    """The osx Extractor
    """

    def _hdiutil_mount(self, temp_dir, file_name, install_dir):
        """Function to mount osx dmg images, extracts the files
           from an image into store and ensure they are
           unmounted on exit.
        """
        # open
        cmd = ["hdiutil", "attach", "-mountpoint", temp_dir, file_name]
        cmd = " ".join(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()
        # find tar.gz files
        cmd = [
            "find",
            temp_dir,
            "-name",
            '"*.tar.gz"',
            "-exec",
            "tar",
            "xvf",
            "'{}'",
            "--directory",
            install_dir,
            "';'",
        ]
        cmd = " ".join(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()
        # close
        cmd = ["hdiutil", "detach", temp_dir]
        cmd = " ".join(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()

    def copy_files(self):
        src = (
            Path(self.extract_temp_dir)
            / "Developer"
            / "NVIDIA"
            / "CUDA-{}".format(self.cu_version)
        )
        dst = self.src_dir

        for f in os.listdir(src):
            source = src / f
            destination = dst / f
            try:
                shutil.copytree(source, destination)
            except NotADirectoryError:
                shutil.copy(source, destination)
            except FileExistsError:
                pass

    def extract(self):
        runfile = os.path.join(self.src_dir, self.cu_blob)
        extract_store_name = "tmpstore"
        extract_temp_dir_name = "tmp"
        self.extract_store = os.path.join(self.src_dir, extract_store_name)
        self.extract_temp_dir = os.path.join(self.src_dir, extract_temp_dir_name)
        os.makedirs(self.extract_store, exist_ok=True)
        os.makedirs(self.extract_temp_dir, exist_ok=True)
        self._hdiutil_mount(self.extract_store, runfile, self.extract_temp_dir)
        self.copy_files()

    def cleanup(self):
        blob_path = os.path.join(self.src_dir, self.cu_blob)
        if os.path.exists(blob_path):
            os.remove(blob_path)

        else:
            pass

        try:
            shutil.rmtree(self.extract_store)

        except FileNotFoundError:
            pass

        try:
            shutil.rmtree(self.extract_temp_dir)

        except FileNotFoundError:
            pass


def getplatform():
    plt = sys.platform
    if plt.startswith("linux"):
        return "linux"
    elif plt.startswith("darwin"):
        return "osx"
    else:
        raise RuntimeError("Unknown platform")


def set_config():
    """Set necessary configurations"""

    cudatoolkit = {"linux": {}, "osx": {}}
    prefix = Path(os.environ["PREFIX"])
    extra_args = dict()
    with open(prefix / "bin" / "cudatoolkit-dev-extra-args.json", "r") as f:
        extra_args = json.loads(f.read())

    # package version decl must match cuda release version
    cudatoolkit["version"] = os.environ["PKG_VERSION"]
    cudatoolkit["name"] = os.environ["PKG_NAME"]
    cudatoolkit["buildnum"] = os.environ["PKG_BUILDNUM"]
    cudatoolkit["version_build"] = extra_args["version_build"]
    cudatoolkit["driver_version"] = extra_args["driver_version"]
    cudatoolkit[
        "base_url"
    ] = f'https://developer.nvidia.com/compute/cuda/{cudatoolkit["version"]}/Prod/'
    cudatoolkit["installers_url_ext"] = f"local_installers/"
    cudatoolkit["patch_url_ext"] = f""
    cudatoolkit[
        "md5_url"
    ] = f'http://developer.download.nvidia.com/compute/cuda/{cudatoolkit["version"]}/Prod/docs/sidebar/md5sum.txt'

    cudatoolkit["linux"] = {
        "blob": f'cuda_{cudatoolkit["version"]}.{cudatoolkit["version_build"]}_{cudatoolkit["driver_version"]}_linux'
    }

    cudatoolkit["osx"] = {
        "blob": f'cuda_{cudatoolkit["version"]}.{cudatoolkit["version_build"]}_mac'
    }

    return cudatoolkit


dispatcher = {"linux": LinuxExtractor, "osx": OsxExtractor}


def _main():

    print("Running Post installation")

    cudatoolkit_config = set_config()

    # get an extractor
    plat = getplatform()
    extractor_impl = dispatcher[plat]
    extractor = extractor_impl(cudatoolkit_config, cudatoolkit_config[plat])

    # create activate and deactivate scripts
    extractor.create_activate_and_deactivate_scripts()

    # download binaries
    extractor.download_blobs()

    # check md5sum
    extractor.check_md5()

    # Extract
    extractor.extract()

    # Cleanup
    extractor.cleanup()


if __name__ == "__main__":
    _main()
