@echo off

REM 将A路径下的所有文件复制到B路径下，相对路径直接写set source=A，当前目录用%cd%指代。

setlocal

set source_path=%cd%
set destination_path=D:\Applications\Blender Foundation\blender-3.6.1\3.6\scripts\addons\xndlib


xcopy /y /s "%source_path%\*" "%destination_path%"

endlocal


