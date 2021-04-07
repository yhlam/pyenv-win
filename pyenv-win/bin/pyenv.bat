@echo off

chcp 1250 >nul


IF EXIST "%~dp0"..\exec.bat (
   del /F /Q "%~dp0"..\exec.bat >nul
)


set preargs=%*

:: Escape # as it will be using as a temporary escape symbol to work around
:: the bizarre behavior of % being both batch variable symbol and URL escape 
:: charactor.
set preargs=%preargs:#=#23%

:: Escape ! so they are not affected by delayed expansion
set preargs=%preargs:!=#21%

setlocal EnableDelayedExpansion

:: Escape %
set preargs=!preargs:%%=#25!

:: Escape the double qoute inside each argument
set args=
FOR %%x IN (%preargs%) DO (
    set arg=%%~x
    set arg=!arg:"=#22!
    set args=!args! "!arg!"
)

:: Replace the temporary escape symbol # to the actual escape symbol %.
:: Note that we need to escape % to %% so that it can be correctly passed
:: to pyenv.vbs
set args=!args:#=%%%%!

setlocal DisableDelayedExpansion

call cscript //nologo "%~dp0"..\libexec\pyenv.vbs %args%
IF EXIST "%~dp0"..\exec.bat (
   "%~dp0"..\exec.bat
)
