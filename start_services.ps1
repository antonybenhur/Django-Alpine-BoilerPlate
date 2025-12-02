# Start all Django Boilerplate services in Windows Terminal tabs

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Build the Windows Terminal command
$wtArgs = @(
    "new-tab",
    "-d", $projectDir,
    "--title", "Django",
    "cmd", "/k", "title Django Server && call venv\Scripts\activate && daphne -b 127.0.0.1 -p 8000 core.asgi:application",
    ";",
    "new-tab",
    "-d", $projectDir,
    "--title", "Tailwind", 
    "cmd", "/k", "title Tailwind && call venv\Scripts\activate && python manage.py tailwind start",
    ";",
    "new-tab",
    "-d", $projectDir,
    "--title", "Celery",
    "cmd", "/k", "title Celery Worker && call venv\Scripts\activate && celery -A core worker -l info -P gevent",
    ";",
    "new-tab",
    "-d", $projectDir,
    "--title", "Beat",
    "cmd", "/k", "title Celery Beat && call venv\Scripts\activate && celery -A core beat -l info"
)

# Launch Windows Terminal
Start-Process "wt" -ArgumentList $wtArgs

Write-Host ""
Write-Host "Services launching in Windows Terminal:" -ForegroundColor Green
Write-Host "  - Django   : http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "  - Tailwind : CSS watcher" -ForegroundColor Cyan
Write-Host "  - Celery   : Background tasks" -ForegroundColor Cyan
Write-Host "  - Beat     : Scheduled tasks" -ForegroundColor Cyan
Write-Host "  - Redis    : localhost:6379" -ForegroundColor Cyan
Write-Host ""

