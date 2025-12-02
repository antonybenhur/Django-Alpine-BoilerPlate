@echo off
echo ========================================
echo   Stopping Dev Environment Services
echo ========================================
echo.

:: Kill all dev server windows by title
echo [1/4] Stopping Django Server...
taskkill /FI "WINDOWTITLE eq Django Server*" /F >nul 2>&1

echo [2/4] Stopping Celery Worker...
taskkill /FI "WINDOWTITLE eq Celery Worker*" /F >nul 2>&1

echo [3/4] Stopping Celery Beat...
taskkill /FI "WINDOWTITLE eq Celery Beat*" /F >nul 2>&1

echo [4/4] Stopping Tailwind Watcher...
taskkill /FI "WINDOWTITLE eq Tailwind Watcher*" /F >nul 2>&1

echo.
echo All application services stopped.
echo.

:: Ask about Redis
set /p STOP_REDIS="Stop Redis container? (y/N): "
if /i "%STOP_REDIS%"=="y" (
    echo Stopping Redis container...
    docker stop django-bp-redis >nul 2>&1
    echo Redis container stopped.
) else (
    echo Redis container left running.
)

echo.
echo ========================================
echo   Cleanup complete!
echo ========================================
pause

