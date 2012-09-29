set pythonPath=c:\Python27
set mongoPath=c:\mongodb\bin\mongod.exe
set mongoDbPath=c:\mongodb\data\db
set elasticSearchPath=c:\elasticsearch-0.19.9\bin\elasticsearch.bat
set appPath=c:\gsapi
set docFolder=%appPath%\doc
set testResultsFile=%docFolder%\testResults.xml

REM cleanup the existing files and directories
rmdir /s /q "%docFolder%\_build"
rmdir /s /q "%docFolder%\_static"
rmdir /s /q "%docFolder%\_templates"
del "%docFolder%\gsapi.rst"
del "%docFolder%\gsapi.models.rst"
del "%docFolder%\gsapi.tests.rst"
del "%docFolder%\gsapi.views.rst"
del "%docFolder%\*.xml"
del "%docFolder%\Makefile"
del "%docFolder%\make.bat"

REM start mongo
REM "%mongoPath%" --dbpath "%mongoDbPath%"

REM run tests
"%pythonPath%\Scripts\nosetests.exe" --with-xunit --xunit-file="%testResultsFile%"

REM get api doc
"%pythonPath%\Scripts\sphinx-apidoc.exe" -F -o doc gsapi

REM build the docs
"%pythonPath%\Scripts\sphinx-build.exe" -b html "%docFolder%" "%docFolder%\_build\html"

REM move the testResults file inside the _build\html dir 
move %testResultsFile% "%docFolder%\_build\html"