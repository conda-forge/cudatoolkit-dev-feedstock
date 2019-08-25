#!/usr/bin/env bash
set -o pipefail

create_symlink_linux() { 
         
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/bin/*;
        do 
            shopt -u nullglob
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};
        done
        shopt -u nullglob

        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/lib64/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done
        shopt -u nullglob
        
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/bin/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};

        done
        shopt -u nullglob
        
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/lib64/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done
        shopt -u nullglob
        
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/libdevice/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done
        shopt -u nullglob
        
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/include/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/include/${link};

        done
        shopt -u nullglob


        ln -sf $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm $CONDA_PREFIX/
        ln -sf $CONDA_PREFIX/lib $CONDA_PREFIX/lib64

}


create_symlink_osx() { 
        
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/bin/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};
        done
        shopt -u nullglob

        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/lib/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done
        shopt -u nullglob

        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/bin/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/bin/${link};

        done
        shopt -u nullglob


        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/lib/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done
        shopt -u nullglob

        
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/libdevice/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/lib/${link};

        done
        shopt -u nullglob
        
        shopt -s nullglob
        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/include/*;
        do 
            link=$(basename "$f");
            ln -sf $f $CONDA_PREFIX/include/${link};

        done
        shopt -u nullglob


        ln -sf $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm $CONDA_PREFIX/


}


UNAME=$(uname)
if [[ $UNAME == "Linux" ]]; then 
   create_symlink_linux

else
    create_symlink_osx

fi