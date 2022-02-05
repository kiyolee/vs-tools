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

find /c "Release|ARM" %SLN% >nul:
if errorlevel 1 goto :bldx86
set _Platforms=ARM ARM64
goto :start
:bldx86
set _Platforms=Win32 x64
goto :start

:start
for %%p in ( %_Platforms% ) do (
  for %%c in ( Release Debug ) do (
    msbuild -t:%TARGET% -p:Platform=%%p -p:Configuration=%%c %_MAXCPU_OPT% %SLN%
  )
)

goto :end

:notexist
echo %SLN% does not exist

:end
endlocal
