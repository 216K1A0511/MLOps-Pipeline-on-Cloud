# scripts/deploy_to_gcp.ps1
# Automates building and pushing the MLOps pipeline to Google Cloud Artifact Registry

param (
    [string]$ProjectId = "YOUR_PROJECT_ID",
    [string]$Region = "us-central1",
    [string]$RepoName = "mlops-docker-repo",
    [string]$ImageName = "gemini-mlops"
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   GCP Artifact Registry Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker not found. Please install Docker." -ForegroundColor Red
    exit 1
}

# 2. Configure Auth
Write-Host "1. Configuring Docker authentication for GCP..." -ForegroundColor Yellow
Write-Host "   (Running: gcloud auth configure-docker ${Region}-docker.pkg.dev)"
# Uncomment to enable auto-auth if gcloud is installed
# gcloud auth configure-docker "${Region}-docker.pkg.dev" --quiet

# 3. Build
Write-Host "2. Building Docker Image..." -ForegroundColor Yellow
docker build -t $ImageName .

# 4. Tag
$GcpTag = "${Region}-docker.pkg.dev/${ProjectId}/${RepoName}/${ImageName}:latest"
Write-Host "3. Tagging image as: $GcpTag" -ForegroundColor Yellow
docker tag "${ImageName}:latest" $GcpTag

# 5. Push
Write-Host "4. Pushing to Artifact Registry..." -ForegroundColor Yellow
Write-Host "   (This requires 'terraform apply' to have finished successfully)"
# docker push $GcpTag

Write-Host "------------------------------------------" -ForegroundColor Green
Write-Host "Build and Tagging Complete!" -ForegroundColor Green
Write-Host "To push, uncomment the 'docker push' line in this script" -ForegroundColor Green
Write-Host "after your Terraform infrastructure is live." -ForegroundColor Green
