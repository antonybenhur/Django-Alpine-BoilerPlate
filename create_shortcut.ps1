# Create Desktop Shortcuts for Django Boilerplate Dev Environment

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath('Desktop')
$ProjectPath = "C:\AntiGravity\DjangoBP"

# Create Start shortcut
$StartShortcut = $WshShell.CreateShortcut((Join-Path $DesktopPath "DjangoBP Dev.lnk"))
$StartShortcut.TargetPath = (Join-Path $ProjectPath "run_dev.bat")
$StartShortcut.WorkingDirectory = $ProjectPath
$StartShortcut.IconLocation = "C:\Windows\System32\shell32.dll,21"
$StartShortcut.Description = "Start Django Boilerplate Development Environment"
$StartShortcut.Save()
Write-Host "Created: DjangoBP Dev.lnk" -ForegroundColor Green

# Create Stop shortcut
$StopShortcut = $WshShell.CreateShortcut((Join-Path $DesktopPath "DjangoBP Stop.lnk"))
$StopShortcut.TargetPath = (Join-Path $ProjectPath "stop_dev.bat")
$StopShortcut.WorkingDirectory = $ProjectPath
$StopShortcut.IconLocation = "C:\Windows\System32\shell32.dll,27"
$StopShortcut.Description = "Stop Django Boilerplate Development Environment"
$StopShortcut.Save()
Write-Host "Created: DjangoBP Stop.lnk" -ForegroundColor Green

Write-Host "`nDesktop shortcuts created successfully!" -ForegroundColor Cyan

