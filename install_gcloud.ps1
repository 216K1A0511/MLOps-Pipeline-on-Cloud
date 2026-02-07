# Install Google Cloud SDK silently
Write-Host "🚀 Installing Google Cloud SDK..." -ForegroundColor Cyan

# Step 1: Download the installer
$installerPath = "$env:TEMP\gcloud_installer.exe"
Write-Host "📥 Downloading Google Cloud SDK installer..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile $installerPath
}
catch {
    Write-Host "❌ Download failed. Please check your internet connection." -ForegroundColor Red
    exit 1
}

# Step 2: Run the installer silently
Write-Host "🔄 Installing Google Cloud SDK (please wait 2-3 minutes)..." -ForegroundColor Yellow
Start-Process -Wait -FilePath $installerPath -ArgumentList "/S", "/NOLAUNCH", "/AllUsers"

# Step 3: Add to PATH
Write-Host "🔧 Adding gcloud to system PATH..." -ForegroundColor Yellow
$gcloudPath = "${env:ProgramFiles(x86)}\Google\Cloud SDK\google-cloud-sdk\bin"
if (-not (Test-Path $gcloudPath)) {
    $gcloudPath = "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin"
}

if (Test-Path $gcloudPath) {
    if ($env:Path -notlike "*$gcloudPath*") {
        [Environment]::SetEnvironmentVariable("Path", "$env:Path;$gcloudPath", [EnvironmentVariableTarget]::User)
        $env:Path += ";$gcloudPath"
        Write-Host "✅ Added $gcloudPath to PATH." -ForegroundColor Green
    }
}
else {
    Write-Host "⚠️ Could not find installation directory automatically." -ForegroundColor Yellow
}

# Step 4: Verify
Write-Host "`n✅ Verifying installation..." -ForegroundColor Green
try {
    $gcloudCmd = Get-Command gcloud -ErrorAction Stop
    & $gcloudCmd --version
    Write-Host "🎉 gcloud installed successfully!" -ForegroundColor Green
}
catch {
    Write-Host "⚠️ gcloud installed but not likely in current PATH yet." -ForegroundColor Yellow
    Write-Host "👉 Please RESTART your terminal/VS Code." -ForegroundColor Cyan
}
