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


install_glibc_214() {
    wget -q http://ftp.gnu.org/gnu/glibc/glibc-2.14.tar.gz
    tar zxf glibc-2.14.tar.gz
    build_dir=$(pwd)/glibc-2.14/build
    install_dir=$(pwd)/glibc-2.14/pkg
    mkdir -p $build_dir
    pushd $build_dir
    ../configure --prefix=$install_dir
    make -j4
    make install
    popd

    export LD_LIBRARY_PATH="${install_dir}/lib:${CONDA_PREFIX}/lib:${LD_LIBRARY_PATH}"
}

# Install GLIBC 2.14 on azure ci
if [[ "$CI" == "azure" ]]; then
    install_glibc_214
fi

python $PREFIX/bin/cudatoolkit-dev-post-install.py

test -d $CONDA_PREFIX/pkgs/cuda-toolkit || exit 1

mkdir -p $CONDA_PREFIX/bin
mkdir -p $CONDA_PREFIX/lib
mkdir -p $CONDA_PREFIX/include

shopt -s nullglob

create_symlink_osx

shopt -u nullglob
