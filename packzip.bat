@echo off
setlocal

set "source_folder=%~dp0xndlib"
for /f "usebackq tokens=1,2,3,4,5,6 delims=/: " %%a in ('%date% %time%') do (
    set "timestamp=%%a%%b%%c%%e%%f"
)
set "zip_file=%~dp0xndlib_%timestamp%.zip"

powershell Compress-Archive -Path "%source_folder%" -DestinationPath "%zip_file%"

echo Done.


exit