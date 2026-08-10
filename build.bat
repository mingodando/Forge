@echo off
REM Always build from main.spec, never from main.py directly -
REM `pyinstaller main.py` silently regenerates the spec and drops the
REM images/font bundling, which crashes the exe on launch.
python -m PyInstaller main.spec --noconfirm