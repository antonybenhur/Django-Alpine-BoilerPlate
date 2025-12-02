@echo off
echo ========================================
echo   Starting Docker Environment
echo ========================================
echo.

:: Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo Building and starting containers...
docker compose up --build

pause
