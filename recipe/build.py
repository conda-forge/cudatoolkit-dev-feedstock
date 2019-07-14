from __future__ import print_function

import argparse
import json
import os
import shutil
from pathlib import Path

def _main(args):

    prefix_dir_path = Path(os.environ["PREFIX"])
    prefix_bin_dir_path = prefix_dir_path / "bin"
    recipe_dir_path = Path(os.environ["RECIPE_DIR"])
    scripts_dir_path = recipe_dir_path / "scripts"
    shutil.copytree(scripts_dir_path, prefix_dir_path / "scripts")

    # Copy cudatoolkit-dev-post-install.py to $PREFIX/bin
    src = recipe_dir_path / "cudatoolkit-dev-post-install.py"
    dst = prefix_bin_dir_path
    shutil.copy(src, dst)
    with open(prefix_bin_dir_path / "cudatoolkit-dev-extra-args.json", "w") as f:
        f.write(json.dumps(args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build script for cudatoolkit-dev")

    parser.add_argument("version", action="store", type=str)
    parser.add_argument("version_build", action="store", type=str)
    parser.add_argument("driver_version", action="store", type=str)
    results = parser.parse_args()
    args = vars(results)
    _main(args)
