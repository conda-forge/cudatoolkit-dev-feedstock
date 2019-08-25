import sys
import os
from numba.cuda.cudadrv.libs import test, get_cudalib
from numba.cuda.cudadrv.nvvm import NVVM


def run_test():
    if not test():
        return False
    nvvm = NVVM()
    print("NVVM version", nvvm.get_version())
    # check pkg version matches lib pulled in
    gotlib = get_cudalib("cublas")
    lookfor = os.environ["PKG_VERSION"]
    return lookfor in gotlib


sys.exit(0 if run_test() else 1)
