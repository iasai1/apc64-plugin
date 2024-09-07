@echo off

set "fileName=%~1"

cd /d "F:\Users\iasai\Desktop\APC64_2\plugin"

python37 -m compileall .\

copy "F:\Users\iasai\Desktop\APC64_2\plugin\__pycache__\%fileName%.cpython-37.pyc" "E:\ProgramData\Ableton\Live 11 Suite\Resources\MIDI Remote Scripts\APC64_Plugin\%fileName%.pyc"