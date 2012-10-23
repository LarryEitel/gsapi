@echo off
set docsFolder=%PROJECT_ROOT%\docs
set staticFolder=%docsFolder%\_static
set testsFolder=%PROJECT_ROOT%\gsapi\tests
set mainApiFile=%docsFolder%\api.rst

REM cleanup the existing files and directories
del /S *.pyc
rmdir /s /q "%docsFolder%\_build\html"
rmdir /s /q "%docsFolder%\_build"
rmdir /s /q "%docsFolder%\_templates"
del "%docsFolder%\*.rst"
del "%docsFolder%\*.jpeg"
del "%docsFolder%\*.txt"
del "%docsFolder%\make.bat"
del "%docsFolder%\Makefile"

REM copy the _static files to doc root folder
xcopy /s /y %staticFolder%  %docsFolder%

REM get api doc
"%PROJECT_ROOT%\%VIRTUALENV%\Scripts\sphinx-apidoc.exe" -F -o %docsFolder% gsapi

REM create the main Api file
echo .. include:: api_intro.rst >> %mainApiFile%
echo .. toctree:: >> %mainApiFile%
echo     :maxdepth: 2 >> %mainApiFile%
echo. >> %mainApiFile%

REM 
FOR /f "delims=" %%a in ('DIR /s /b %testsFolder%\test*.py') do ( 
	IF NOT "%%~na" == "__init__.py" (
 		for /D %%I in (%%a\..) DO (
 			echo     api_%%~nxI.%%~na >> %mainApiFile%
 		)	
  	)
)
		
REM run tests and append the rest of .rst files to the mainApiFile
FOR /f "delims=" %%a in ('DIR /s /b %testsFolder%\test*.py') do (
	for /D %%I in (%%a\..) DO (
 		nosetests -v --nocapture %%a >> %docsFolder%\api_%%~nxI.%%~na.rst
  	)
)

REM build the docs
"%PROJECT_ROOT%\%VIRTUALENV%\Scripts\sphinx-build.exe" -b html "%docsFolder%" "%docsFolder%\_build\html"
