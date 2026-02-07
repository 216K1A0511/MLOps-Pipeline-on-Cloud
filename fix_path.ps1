# fix_path.ps1 - Immediate PATH fix for gcloud
Write-Host "🔧 Fixing gcloud PATH issue..." -ForegroundColor Cyan

# Method 1: Check if gcloud exists in default location
$gcloudPaths = @(
    "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
    "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
    "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
)

foreach ($path in $gcloudPaths) {
    if (Test-Path $path) {
        Write-Host "✅ Found gcloud at: $path" -ForegroundColor Green
        
        # Get directory
        $dir = [System.IO.Path]::GetDirectoryName($path)

        # Add to current session PATH
        $env:Path += ";$dir"
        
        # Test gcloud
        try {
            & $path --version | Select-Object -First 1
            Write-Host "🎉 gcloud is now accessible!" -ForegroundColor Green
            
            # Make permanent
            $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
            if ($currentPath -notlike "*$dir*") {
                [Environment]::SetEnvironmentVariable("Path", "$currentPath;$dir", [EnvironmentVariableTarget]::User)
                Write-Host "💾 Added to permanent User PATH" -ForegroundColor Green
            }
            break
        }
        catch {
            Write-Host "⚠️ Could not run gcloud from this path" -ForegroundColor Yellow
        }
    }
}

# Method 2: Manual search if not found
Write-Host "`n🔍 Deep searching for gcloud installation (this might take a moment)..." -ForegroundColor Yellow
$found = $false
# Look in likely places first to save time
$searchPaths = @("C:\Program Files", "C:\Program Files (x86)", "$env:USERPROFILE\AppData\Local")

foreach ($searchRoot in $searchPaths) {
    if ($found) { break }
    if (Test-Path $searchRoot) {
        Get-ChildItem -Path $searchRoot -Recurse -Filter "gcloud.cmd" -ErrorAction SilentlyContinue | ForEach-Object {
            $path = $_.FullName
            $dir = $_.DirectoryName
            Write-Host "Found: $path" -ForegroundColor Gray
            
            if (-not $found) {
                try {
                    & $path --version | Out-Null
                    Write-Host "✅ Verified working gcloud at: $dir" -ForegroundColor Green
                    
                    $env:Path += ";$dir"
                    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
                    if ($currentPath -notlike "*$dir*") {
                        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$dir", [EnvironmentVariableTarget]::User)
                        Write-Host "💾 Added to permanent User PATH" -ForegroundColor Green
                    }
                    $found = $true
                }
                catch { }
            }
        }
    }
}

if (-not $found) {
    Write-Host "❌ gcloud not found. Please install it first." -ForegroundColor Red
    Write-Host "Download from: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -ForegroundColor Yellow
}
else {
    Write-Host "`n🎉 Success! Now try running your deployment script again." -ForegroundColor Green
}
