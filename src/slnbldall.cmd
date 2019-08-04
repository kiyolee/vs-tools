@echo off
setlocal

if .%1. == .. goto :end
set SLN=%1

if .%2. == .. goto :notarget
set TARGET=%2
goto :nexttarget
:notarget
set TARGET=Build
:nexttarget

for %%p in ( Win32 x64 ) do (
  for %%c in ( Release Debug ) do (
    msbuild %SLN% /m /t:%TARGET% /p:Platform=%%p /p:Configuration=%%c
  )
)

:end
endlocal
