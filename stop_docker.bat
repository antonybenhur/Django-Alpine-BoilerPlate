@echo off
echo ========================================
echo   Stopping Docker Environment
echo ========================================
echo.

docker compose down

echo.
echo Containers stopped.
pause
