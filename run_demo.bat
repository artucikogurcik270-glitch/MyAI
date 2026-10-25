@echo off
title Tumaris Demo
color 0E

cd /d D:\Project
python client.py demo

if %errorlevel% neq 0 (
    echo.
    echo Error running demo. Make sure Python is installed.
    pause
)

pause
