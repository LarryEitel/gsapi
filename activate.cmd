@echo off

set PYTHON_ROOT=C:\Python27
set PROJECT_NAME=gsapi

REM The name of the virtualenv when you ran:
REM virtualenv venv
set VIRTUALENV=venv

REM Grab the parent of current 'CD' directory
for %%F in ("%CD%") do set PROJECTS_ROOT=%%~dpF

set PYTHONHOME=%PYTHON_ROOT%
set PROJECT_ROOT=%PROJECTS_ROOT%%PROJECT_NAME%

set PATH=%PATH%;%PROJECT_ROOT%scripts\windows

set PYTHONPATH=%PROJECTS_ROOT%;%PROJECT_ROOT%;%PROJECT_ROOT%\%VIRTUALENV%\Lib;%PROJECT_ROOT%\%VIRTUALENV%\Lib\site-packages;%PYTHON_ROOT%;%PYTHON_ROOT%\Lib;%PYTHON_ROOT%\Lib\site-packages

cd %PROJECT_NAME%

REM Activate virtual environment
%PROJECT_ROOT%\%VIRTUALENV%\Scripts\activate.bat

