# simple_fix.ps1 - Fixes gcloud path for the current session
Write-Host "--- GCloud Path Fixer ---" -ForegroundColor Cyan

# 1. common installation paths
$possiblePaths = @(
    "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin",
    "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin",
    "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin",
    "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"
)

$gcloudFound = $false

foreach ($path in $possiblePaths) {
    if (Test-Path "$path\gcloud.cmd") {
        Write-Host "Found gcloud at: $path" -ForegroundColor Green
        
        # Add to current session PATH
        $env:Path = "$path;$env:Path"
        $gcloudFound = $true
        break
    }
}

# 2. If not found, try to piggyback on System Path (CMD install)
if (-not $gcloudFound) {
    $systemPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($systemPath -like "*Google*Cloud*") {
        Write-Host "Found Google Cloud in System Path. Importing..." -ForegroundColor Yellow
        $env:Path = "$systemPath;$env:Path"
        $gcloudFound = $true
    }
}

if ($gcloudFound) {
    Write-Host "Success! Verifying..." -ForegroundColor Cyan
    try {
        gcloud.cmd --version
        Write-Host "GCloud is ready." -ForegroundColor Green
    }
    catch {
        Write-Host "Still having trouble running 'gcloud.cmd'. Try restarting your terminal." -ForegroundColor Red
    }
}
else {
    Write-Host "Could not find gcloud. Please verify installation." -ForegroundColor Red
}
