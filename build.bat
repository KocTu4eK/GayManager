@echo off
mkdir output

pyrcc5 -o source/resources.py resources.qrs
nuitka --windows-icon-from-ico=icon.ico --windows-disable-console --output-dir=output -o output/GayManager --follow-imports source/main.py
