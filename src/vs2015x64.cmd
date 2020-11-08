@echo off
setlocal
set _VSVER_=VS2015-x64
set _GCT_=
set _CONTITLE_=
for %%i in ( get_console_title.cmd ) do set "_GCT_=%%~$PATH:i"
if "%_GCT_%" == "" goto :notitle
for /f "delims=" %%i in ('get_console_title.cmd "%~n0"') do set "_CONTITLE_=%%i"
:notitle
if "%_CONTITLE_%" == "" goto :deftitle
set _CONTITLE_=%_CONTITLE_% - %_VSVER_%
goto :dovc
:deftitle
set _CONTITLE_=%_VSVER_%
:dovc
title %_CONTITLE_%
endlocal
pushd .
if exist "%~dp0\vcvarsreset.cmd" call "%~dp0\vcvarsreset.cmd"
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\vc\vcvarsall.bat" amd64 %*
popd
