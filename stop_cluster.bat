@echo off
title Tumaris AI Cluster - Shutdown
color 0C

echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║         TUMARIS AI CLUSTER - Stopping Nodes           ║
echo  ╚════════════════════════════════════════════════════════╝
echo.

echo [SHUTDOWN] Stopping all Tumaris services...
echo.

taskkill /FI "WindowTitle eq Tumaris-Router*" /F >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Router stopped
) else (
    echo [SKIP] Router not running
)

taskkill /FI "WindowTitle eq Tumaris-Ear*" /F >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ear service stopped
) else (
    echo [SKIP] Ear service not running
)

taskkill /FI "WindowTitle eq Tumaris-Brain*" /F >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Brain service stopped
) else (
    echo [SKIP] Brain service not running
)

taskkill /FI "WindowTitle eq Tumaris-Styler*" /F >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Styler service stopped
) else (
    echo [SKIP] Styler service not running
)

taskkill /FI "WindowTitle eq Tumaris-Voice*" /F >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Voice service stopped
) else (
    echo [SKIP] Voice service not running
)

echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║           All Tumaris Services Stopped                ║
echo  ╚════════════════════════════════════════════════════════╝
echo.
pause
