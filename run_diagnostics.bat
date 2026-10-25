@echo off
title Tumaris Diagnostics
color 0E

cd /d D:\Project
python diagnostics.py

if %errorlevel% neq 0 (
    echo.
    echo Error running diagnostics.
)

pause
