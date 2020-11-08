@echo off
setlocal
set _VSVER_=VS2019-x64
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
set _VCVARS_HEAD_=C:\Program Files (x86)\Microsoft Visual Studio\2019
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
set _VCVARS_HEAD_=
set _VCVARS_TAIL_=
popd
