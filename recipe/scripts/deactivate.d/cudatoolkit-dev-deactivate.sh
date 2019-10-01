#!/usr/bin/env bash
set -o pipefail

remove_symlink_linux() {

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/bin/*;
        do  
            to_unlink=$(basename ${f});
            
            if [ -L "$CONDA_PREFIX/bin/${to_unlink}" ]; then
                unlink $CONDA_PREFIX/bin/${to_unlink};
            fi 

        done


        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/lib64/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/lib/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/lib/${to_unlink};
            fi 
            
        done


        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/bin/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/bin/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/bin/${to_unlink};
            fi 
            
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/lib64/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/lib/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/lib/${to_unlink};
            fi 
            
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/libdevice/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/lib/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/lib/${to_unlink};
            fi 
            
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/include/*;
        do 
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/include/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/include/${to_unlink};
            fi 
        done    
}


remove_symlink_osx() {

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/bin/*;
        do  
            to_unlink=$(basename ${f});
            
            if [ -L "$CONDA_PREFIX/bin/${to_unlink}" ]; then
                unlink $CONDA_PREFIX/bin/${to_unlink};
            fi 

        done


        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/lib/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/lib/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/lib/${to_unlink};
            fi 
            
        done


        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/bin/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/bin/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/bin/${to_unlink};
            fi 
            
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/lib/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/lib/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/lib/${to_unlink};
            fi 
            
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/nvvm/libdevice/*;
        do  
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/lib/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/lib/${to_unlink};
            fi 
            
        done

        for f in $CONDA_PREFIX/pkgs/cuda-toolkit/include/*;
        do 
            to_unlink=$(basename ${f});

            if [ -L "$CONDA_PREFIX/include/${to_unlink}" ]; then
            unlink $CONDA_PREFIX/include/${to_unlink};
            fi 
        done    
}


shopt -s nullglob

UNAME=$(uname)
if [[ $UNAME == "Linux" ]]; then 
   remove_symlink_linux

else
   remove_symlink_osx

fi

shopt -u nullglob
