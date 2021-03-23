#!/usr/bin/env bash
set -o pipefail

python $PREFIX/bin/cudatoolkit-dev-post-install.py


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


create_symlink_osx() { 
        
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/bin/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/lib/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/bin/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};

        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/lib/*;
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

}

# Install GLIBC 2.14 on azure ci
if [[ "$CI" == "azure" ]]; then
    wget http://ftp.gnu.org/gnu/glibc/glibc-2.14.tar.gz
    tar zxvf glibc-2.14.tar.gz
    mkdir -p glibc-2.14/build
    pushd glibc-2.14/build
    ../configure --prefix=/opt/glibc-2.14
    make -j4
    sudo make install
    popd

    export LD_LIBRARY_PATH="/opt/glibc-2.14/lib:${$LD_LIBRARY_PATH}"
fi

test -d $CONDA_PREFIX/pkgs/cuda-toolkit || exit 1

mkdir -p $CONDA_PREFIX/bin
mkdir -p $CONDA_PREFIX/lib
mkdir -p $CONDA_PREFIX/include

shopt -s nullglob

UNAME=$(uname)
if [[ $UNAME == "Linux" ]]; then 
    create_symlink_linux
else
    create_symlink_osx

fi

shopt -u nullglob
