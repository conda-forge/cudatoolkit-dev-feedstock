python %PREFIX%\bin\cudatoolkit-dev-post-install.py
if errorlevel 1 exit 1

if not exist "%CONDA_PREFIX%\Library\bin\" md "%CONDA_PREFIX%\Library\bin"
if not exist "%CONDA_PREFIX%\Library\lib\" md "%CONDA_PREFIX%\Library\lib"
if not exist "%CONDA_PREFIX%\Library\include\" md "%CONDA_PREFIX%\Library\include"
if errorlevel 1 exit 1


for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\bin\*") do (
    if not exist "%CONDA_PREFIX%\Library\bin\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\bin\%%~NXA" "%%~A"
)

for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\lib\x64\*") do (
    if not exist "%CONDA_PREFIX%\Library\lib\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\lib\%%~NXA" "%%~A"
)

for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\lib\*") do (
    if not exist "%CONDA_PREFIX%\Library\lib\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\lib\%%~NXA" "%%~A"
)

for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\include\*") do (
    if not exist "%CONDA_PREFIX%\Library\include\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\include\%%~NXA" "%%~A"
)


for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\nvvm\bin\*") do (
    if not exist "%CONDA_PREFIX%\Library\bin\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\bin\%%~NXA" "%%~A"
)

for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\nvvm\lib\x64\*") do (
    if not exist "%CONDA_PREFIX%\Library\lib\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\lib\%%~NXA" "%%~A"
)

for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\nvvm\lib\*") do (
    if not exist "%CONDA_PREFIX%\Library\lib\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\lib\%%~NXA" "%%~A"
)

for %%A in ("%CONDA_PREFIX%\pkgs\cuda-toolkit\nvcc\libdevice\*") do (
    if not exist "%CONDA_PREFIX%\Library\bin\%%~NXA" mklink /H "%CONDA_PREFIX%\Library\bin\%%~NXA" "%%~A"
)

if not exist "%CONDA_PREFIX%\Library\bin\cudadevrt.lib" mklink /H "%CONDA_PREFIX%\Library\bin\cudadevrt.lib" "%CONDA_PREFIX%\Library\lib\cudadevrt.lib"

if errorlevel 1 exit 1
