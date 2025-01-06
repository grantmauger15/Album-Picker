@echo off
echo Adding the current directory to the PATH...

:: Get the current directory
set CURRENT_DIR=%cd%

:: Check if the current directory is already in PATH
for %%i in ("%PATH:;=" "%") do if "%%~i"=="%CURRENT_DIR%" (
    echo The current directory is already in PATH.
    goto :END
)

:: Add the current directory to the PATH
setx PATH "%PATH%;%CURRENT_DIR%"
echo Successfully added %CURRENT_DIR% to PATH.

:END
echo Installation complete! You can now use the 'album' command.
pause
