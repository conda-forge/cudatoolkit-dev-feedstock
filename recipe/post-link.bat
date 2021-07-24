python %PREFIX%\bin\cudatoolkit-dev-post-install.py
if errorlevel 1 exit 1

for /D %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\*") do (

    if not exist "%CONDA_PREFIX%\Library\%%~NA\" md "%CONDA_PREFIX%\Library\%%~NA"
)

for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\*") do (
    if not exist "%CONDA_PREFIX%\Library\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\%%~NXA" "%%~A"
)
if errorlevel 1 exit 1
