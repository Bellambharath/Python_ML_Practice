@echo off
rem Define the paths
set input_file="C:\Users\BharathKumar_Bellam\Python for DS-ML\Py-DS-ML-Bootcamp-master\Refactored_Py_DS_ML_Bootcamp-master\PythonForDL.ipynb"
set temp_file="C:\Users\BharathKumar_Bellam\Python for DS-ML\Py-DS-ML-Bootcamp-master\Refactored_Py_DS_ML_Bootcamp-master\Temp_PythonForDL.ipynb"

rem Execute the notebook with papermill using Python and save to a temporary file
"C:\Program Files\Python310\python.exe" -m papermill %input_file% %temp_file%

rem Overwrite the original file with the temporary file
move /Y %temp_file% %input_file%

pause
