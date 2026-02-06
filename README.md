# Gemini MLOps Pipeline

## Quick Start

To run the pipeline, execute the PowerShell script in the root directory:

```powershell
.\quick_start.ps1
```

This script will:
1. Check for your Gemini API Key.
2. Install dependencies.
3. Generate sample data.
4. Run the ML pipeline.

## Pipeline Versions

### 1. Minimal Production Pipeline (Recommended for testing)
```powershell
python gemini-mlops-production/src/pipeline/minimal_pipeline.py
```

### 2. Full Pipeline (Original)
```powershell
.\quick_start.ps1
```

### 3. API Server (Web App)
```powershell
python gemini-mlops-production/src/api/server.py
```

## API Quota Note
If you see a `429 Quota Exceeded` error, it means your Gemini API free tier limit has been reached. Please wait a minute before retrying.

## Troubleshooting
**Git Error:** If you see "nested repository" errors, it's because the `gemini-mlops-production` folder had its own `.git` folder. We have removed it to allow adding files to the main repository.
