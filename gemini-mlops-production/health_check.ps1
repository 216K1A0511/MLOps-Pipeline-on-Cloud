Write-Host "🔍 Gemini MLOps Pipeline Health Check" -ForegroundColor Cyan
Write-Host "====================================="

# 1. Check Python environment
Write-Host "1. Python Environment:"
python --version
pip list | Select-String "google-generative|pandas|numpy" | Select-Object -First 5

# 2. Check Gemini API connection
Write-Host "`n2. Gemini API Connection:"
$env:GEMINI_API_KEY = "AIzaSyDN0Jb5jF9djDdF5Y3yqkpPvCa21VasLKw" # Using your updated key
python -c @"
import google.generativeai as genai
import os
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    # Use pro-latest to avoid 404
    model = genai.GenerativeModel('gemini-pro-latest')
    model.generate_content('Test')
    print('✅ Gemini API accessible')
except Exception as e:
    print(f'❌ Gemini API error: {e}')
"@

# 3. Check project structure
Write-Host "`n3. Project Structure:"
$dirs = "src", "configs", "data", "models", "logs", "reports"
foreach ($dir in $dirs) {
    if (Test-Path $dir) { Write-Host "   ✅ $dir" -ForegroundColor Green }
    else { Write-Host "   ❌ $dir (missing)" -ForegroundColor Red }
}

# 4. Check Docker
Write-Host "`n4. Docker Check:"
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "   ✅ Docker installed" -ForegroundColor Green
    docker --version
}
else {
    Write-Host "   ⚠️  Docker not found (optional)" -ForegroundColor Yellow
}

Write-Host "`n📊 HEALTH CHECK SUMMARY:"
Write-Host "====================================="
if ((Test-Path "src") -and (Test-Path "configs")) {
    Write-Host "✅ Pipeline setup looks good!" -ForegroundColor Green
}
else {
    Write-Host "❌ Issues detected. Check missing folders above." -ForegroundColor Red
}
