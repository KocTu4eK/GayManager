@set @x=0; /*
@echo off
ver |> NUL find /v "5." && if "%~1" == "" cscript.exe //nologo //e:jscript "%~f0" & exit /b

cd /d %~dp0
pyrcc5 -o source/resources.py resources.qrs
py source/main.py

exit /B
*/new ActiveXObject('Shell.Application').ShellExecute (WScript.ScriptFullName, 'Admin', '', 'runas', 1);
