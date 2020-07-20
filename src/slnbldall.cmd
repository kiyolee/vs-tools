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

for %%p in ( Win32 x64 ) do (
  for %%c in ( Release Debug ) do (
    msbuild -t:%TARGET% -p:Platform=%%p -p:Configuration=%%c %_MAXCPU_OPT% %SLN%
  )
)

:end
endlocal
