@echo off
setlocal

if .%1. == .. goto :end
set SLN=%1

if .%2. == .. goto :notarget
set TARGET=%2
goto :havetarget
:notarget
set TARGET=Build
:havetarget

if .%3. == .. goto :nomaxcpu
set _MAXCPU_OPT=-m:%3
goto :havemaxcpu
:nomaxcpu
set _MAXCPU_OPT=-m
:havemaxcpu

if not exist %SLN% goto :notexist

set _Platform_arm32=
set _Platform_arm64=
set _Platform_win32=
set _Platform_x86=
set _Platform_x64=

find /c "Release|ARM." %SLN% >nul:
if errorlevel 1 goto :noarm32
set _Platform_arm32=ARM
:noarm32
find /c "Release|ARM64." %SLN% >nul:
if errorlevel 1 goto :noarm64
set _Platform_arm64=ARM64
:noarm64
find /c "Release|Win32." %SLN% >nul:
if errorlevel 1 goto :nowin32
set _Platform_win32=Win32
:nowin32
find /c "Release|x86." %SLN% >nul:
if errorlevel 1 goto :nox86
set _Platform_x86=x86
:nox86
find /c "Release|x64." %SLN% >nul:
if errorlevel 1 goto :nox64
set _Platform_x64=x64
:nox64

:start
for %%p in ( %_Platform_x64% %_Platform_x86% %_Platform_win32% %_Platform_arm64% %_Platform_arm32% ) do (
  for %%c in ( Release Debug ) do (
    msbuild -t:%TARGET% -p:Platform=%%p -p:Configuration=%%c %_MAXCPU_OPT% %SLN%
  )
)

goto :end

:notexist
echo %SLN% does not exist

:end
endlocal
