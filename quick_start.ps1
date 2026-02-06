# quick_start.ps1 - Complete setup and run for Windows
$ErrorActionPreference = "Stop"

Write-Host "Gemini MLOps Pipeline Quick Start" -ForegroundColor Cyan

# 0. Check System Requirements
Write-Host "Checking system requirements..."
# Check Node.js
if (Get-Command node -ErrorAction SilentlyContinue) { Write-Host "Node.js detected" } else { Write-Host "Node.js not found (Web App skipped)" }

# 1. Check for Gemini API key
if (-not $env:GEMINI_API_KEY) {
    if (Test-Path .env) {
        Write-Host "Loading API key from .env file..." -ForegroundColor Yellow
        Get-Content .env | ForEach-Object {
            if ($_ -match "GEMINI_API_KEY=(.*)") {
                $env:GEMINI_API_KEY = $matches[1]
            }
        }
    }
}

if (-not $env:GEMINI_API_KEY) {
    Write-Host "GEMINI_API_KEY environment variable not set and not found in .env" -ForegroundColor Red
    Write-Host "Run: `$env:GEMINI_API_KEY = 'your-key-here'"
    exit
}

Write-Host "Gemini API key found" -ForegroundColor Green

# 2. Create project structure
Write-Host "Creating project structure..."
$dirs = "data/raw", "data/processed", "data/generated", "models/registry", "models/deployed", "logs", "reports", "configs"
foreach ($dir in $dirs) { 
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null 
    }
}

# 3. Install dependencies
Write-Host "Installing dependencies from requirements.txt..."
pip install -q -r requirements.txt

# 4. Generate sample data
Write-Host "Generating sample data..."
python src/data_processing/generate_sample_data.py

# 5. Run pipeline
Write-Host "Running ML pipeline..."
# Enable Mock Mode by default for robust testing
$env:USE_MOCK = "true"
Write-Host "Using mock mode (no API calls). Set USE_MOCK=false to use real Gemini API." -ForegroundColor Yellow

$pipelineArgs = @(
    "-m", "src.pipeline.pipeline",
    "--data-path", "data/raw/sample_data.csv",
    "--task-type", "classification",
    "--run-id", "quick_start_ps1"
)

if ($env:USE_MOCK -eq "true") {
    $pipelineArgs += "--use-mock"
}

python @pipelineArgs

Write-Host "Setup complete! Check reports/ directory for results" -ForegroundColor Green
