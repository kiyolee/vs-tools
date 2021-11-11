@echo off
set _VSVER_=2010
setlocal
set _VSVER_TITLE_=VS%_VSVER_%
set _GCT_=
set _CONTITLE_=
for %%i in ( get_console_title.cmd ) do set "_GCT_=%%~$PATH:i"
if "%_GCT_%" == "" goto :notitle
for /f "delims=" %%i in ('get_console_title.cmd "%~n0"') do set "_CONTITLE_=%%i"
:notitle
if "%_CONTITLE_%" == "" goto :deftitle
set _CONTITLE_=%_CONTITLE_% - %_VSVER_TITLE_%
goto :dovc
:deftitle
set _CONTITLE_=%_VSVER_TITLE_%
:dovc
title %_CONTITLE_%
endlocal
pushd .
if exist "%~dp0vcvarsreset.cmd" call "%~dp0vcvarsreset.cmd"
call "%ProgramFiles(x86)%\Microsoft Visual Studio 10.0\vc\vcvarsall.bat" x86 %*
set _VSVER_=
popd
