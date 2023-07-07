import sys
import os
#driver located in $PREFIX/lib/stubs
os.environ["NUMBA_CUDA_DRIVER"] = os.environ["PREFIX"] + "/lib/stubs/libcuda.so"
from numba.cuda.cudadrv.libs import test
from numba.cuda.cudadrv.nvvm import NVVM


def run_test():

    if not test():
        return False
    nvvm = NVVM()
    print("NVVM version", nvvm.get_version())
    return nvvm.get_version() is not None


sys.exit(0 if run_test() else 1)
