@echo off
set _VSVER_=2019
setlocal
set _VSVER_TITLE_=VS%_VSVER_%-x64
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
set _VCVARS_HEAD_=%ProgramFiles(x86)%\Microsoft Visual Studio\%_VSVER_%
set _VCVARS_TAIL_=VC\Auxiliary\Build\vcvars64.bat
if exist "%_VCVARS_HEAD_%\Enterprise\%_VCVARS_TAIL_%" goto :ente
if exist "%_VCVARS_HEAD_%\Professional\%_VCVARS_TAIL_%" goto :prof
if exist "%_VCVARS_HEAD_%\Community\%_VCVARS_TAIL_%" goto :comm
goto :end
:ente
call "%_VCVARS_HEAD_%\Enterprise\%_VCVARS_TAIL_%" %*
goto :end
:prof
call "%_VCVARS_HEAD_%\Professional\%_VCVARS_TAIL_%" %*
goto :end
:comm
call "%_VCVARS_HEAD_%\Community\%_VCVARS_TAIL_%" %*
goto :end
:end
set _VSVER_=
set _VCVARS_HEAD_=
set _VCVARS_TAIL_=
popd
