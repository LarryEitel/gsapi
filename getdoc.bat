@echo off
set docsFolder=%PROJECT_ROOT%\docs
set confFolder=%docsFolder%\conf
set testsFolder=%PROJECT_ROOT%\gsapi\tests
set mainApiFile=%docsFolder%\api.rst

REM cleanup the existing files and directories
del /S *.pyc
rmdir /s /q "%docsFolder%\_build\html"
rmdir /s /q "%docsFolder%\_build"
rmdir /s /q "%docsFolder%\_static"
rmdir /s /q "%docsFolder%\_templates"
del "%docsFolder%\Makefile"
del "%docsFolder%\make.bat"
del "%docsFolder%\*.rst"
del "%docsFolder%\conf.py"

REM copy the configuration file to doc root folder
cp %confFolder%\conf.py.orig %docsFolder%\conf.py
cp %confFolder%\index.rst.orig %docsFolder%\index.rst
cp %confFolder%\intro.rst.orig %docsFolder%\intro.rst

REM get api doc
"%PROJECT_ROOT%\%VIRTUALENV%\Scripts\sphinx-apidoc.exe" -F -o %docsFolder% gsapi

REM create the main Api file
echo .. include:: intro.rst >> %mainApiFile%
echo .. toctree:: >> %mainApiFile%
echo     :maxdepth: 2 >> %mainApiFile%
echo. >> %mainApiFile%
FOR /f "delims=" %%a in ('DIR /s /b %testsFolder%\test*.py') do ( IF NOT "%%~na" == "__init__.py" (echo     %%~na >> %mainApiFile%))

REM run tests and append the rest of .rst files to the mainApiFile
FOR /f "delims=" %%a in ('DIR /s /b %testsFolder%\test*.py') do (nosetests -v --nocapture %%a >> %docsFolder%\%%~na.rst)

REM build the docs
"%PROJECT_ROOT%\%VIRTUALENV%\Scripts\sphinx-build.exe" -b html "%docsFolder%" "%docsFolder%\_build\html"
