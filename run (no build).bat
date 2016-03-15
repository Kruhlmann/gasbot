title Chat Bot
color
@echo off
cls
set PATH=%PATH%;%cd%\includes\ansicon
includes\ansicon\ansicon.exe -i
python -B bot.py
pause
