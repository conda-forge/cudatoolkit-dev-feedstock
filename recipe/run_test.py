import sys
import os
#driver located in $PREFIX/lib/stubs in linux, below line works for windows too
#In windows, the driver is located in $PREFIX/Library/bin/stubs
platform = sys.platform
if platform == "win32":
    os.environ["NUMBA_CUDA_DRIVER"] = os.path.join(os.environ["PREFIX"], "Library", "bin", "stubs", "cuda.dll")
else:
    os.environ["NUMBA_CUDA_DRIVER"] = os.path.join(os.environ["PREFIX"], "lib", "stubs", "libcuda.so")
from numba.cuda.cudadrv.libs import test
from numba.cuda.cudadrv.nvvm import NVVM


def run_test():

    if not test():
        return False
    nvvm = NVVM()
    print("NVVM version", nvvm.get_version())
    return nvvm.get_version() is not None


sys.exit(0 if run_test() else 1)
