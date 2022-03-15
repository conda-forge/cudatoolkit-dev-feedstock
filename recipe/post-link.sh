#!/usr/bin/env bash
set -o pipefail


create_symlink_linux() {

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/bin/*;
        do
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/lib64/*;
        do
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/bin/*;
        do
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};

        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/lib64/*;
        do
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/libdevice/*;
        do
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/include/*;
        do
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/include/${link};

        done


        ln -sf $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm $CONDA_PREFIX/
        ln -sf $CONDA_PREFIX/lib $CONDA_PREFIX/lib64

}

fix_resolve_path() {
    if [[ "${OSTYPE}" == "darwin"* ]]; then
        searchstr='dirname \"\$\(readlink \-\- \"\$0\"\)\"'
    else
        searchstr='dirname \"\$\(readlink \-f \-\- \"\$0\"\)\"'
    fi

    sed -i "s/.*dirname.*/CUDA_BIN\=\\$\(${searchstr}\)/" $CONDA_PREFIX/pkgs/cuda-toolkit/bin/nvvp
    sed -i "s/.*BASH_SOURCE.*/DIR\=\\$\(${searchstr}\)/" $CONDA_PREFIX/pkgs/cuda-toolkit/bin/nsys
    sed -i "s/.*BASH_SOURCE.*/DIR\=\\$\(${searchstr}\)/" $CONDA_PREFIX/pkgs/cuda-toolkit/bin/nsys-ui
    sed -i "s/.*BASH_SOURCE.*/DIR\=\\$\(cd \"\\$\(${searchstr}\)\" \&\& pwd \)/" $CONDA_PREFIX/pkgs/cuda-toolkit/bin/nsight-sys

}

python $PREFIX/bin/cudatoolkit-dev-post-install.py

test -d $CONDA_PREFIX/pkgs/cuda-toolkit || exit 1

mkdir -p $CONDA_PREFIX/bin
mkdir -p $CONDA_PREFIX/lib
mkdir -p $CONDA_PREFIX/include

shopt -s nullglob

create_symlink_linux

fix_resolve_path

shopt -u nullglob
