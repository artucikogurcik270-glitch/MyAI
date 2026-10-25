@echo off
title Tumaris Client - Interactive Mode
color 0B

cd /d D:\Project
python client.py

if %errorlevel% neq 0 (
    echo.
    echo Error running client. Make sure Python is installed.
    pause
)
