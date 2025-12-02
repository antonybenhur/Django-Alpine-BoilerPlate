@echo off
echo ========================================
echo   Django Boilerplate Dev Environment
echo ========================================
echo.

:: Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

:: Start Redis container
echo [1/2] Starting Redis container...
docker start django-bp-redis >nul 2>&1
if errorlevel 1 (
    docker run -d --name django-bp-redis -p 6379:6379 redis:alpine >nul 2>&1
)
timeout /t 2 /nobreak >nul
echo       Redis ready on localhost:6379

echo.
echo [2/2] Launching services in Windows Terminal...
echo.

:: Use PowerShell to launch Windows Terminal with tabs
powershell -ExecutionPolicy Bypass -File "%~dp0start_services.ps1"

echo.
echo ========================================
echo   All services started!
echo ========================================
echo.
pause
