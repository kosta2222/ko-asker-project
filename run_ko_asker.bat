set PATH=""

set CONDA_HOME=B:\anaconda3\Scripts
set COND_PY_HOME=B:\anaconda3
set CONDA_PY_Lib=%CONDA_PY_HOME%\Lib
set CONDA_PY_site_packages=%CONDA_PY_LIB%\site-packages
set PYTHONHOME=%CONDA_PY_HOME%
set PYTHONPATH=%CONDA_PY_site_packages%
set CONDA_LIBR_BIN=B:\anaconda3\Library\bin
set PATH=%CONDA_HOME%;%COND_PY_HOME%;%CONDA_LIBR_BIN%;
start cmd /K conda.bat activate ./envs 


