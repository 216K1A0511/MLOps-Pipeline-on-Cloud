# deploy_to_gcp.ps1 - Authenticates and Deploys to Cloud Run/Artifact Registry (Improved)

$ErrorActionPreference = "Stop"

# Configuration
$PROJECT_ID = "galvanic-host-425316-j9"
$REGION = "us-central1"
$REPO_NAME = "mlops-docker-repo"
$IMAGE_TAG = "latest"

# Add Terraform to Path (if in local project)
if (Test-Path "$PSScriptRoot\terraform\terraform.exe") {
    $env:Path += ";$PSScriptRoot\terraform"
    Write-Host "Added local Terraform to Path."
}

Write-Host "Starting GCP Deployment..."

# --- AUTO-FIND GCLOUD ---
function Get-GcloudPath {
    if (Get-Command "gcloud" -ErrorAction SilentlyContinue) { return "gcloud" }
    if (Get-Command "gcloud.cmd" -ErrorAction SilentlyContinue) { return "gcloud.cmd" }
    
    $candidates = @(
        "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
        "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
        "$env:LOCALAPPDATA\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
        "$env:USERPROFILE\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    )
    
    foreach ($c in $candidates) {
        if (Test-Path $c) { return $c }
    }
    return $null
}

$gcloud = Get-GcloudPath

if (-not $gcloud) {
    Write-Host "ERROR: gcloud not found. Please install Google Cloud SDK."
    exit 1
}

Write-Host "Using gcloud at: $gcloud"

# 1. Check Auth & Set Token for Terraform
Write-Host "Checking GCP Authentication..."
try {
    $token = & $gcloud auth print-access-token
    if (-not $token) { throw "No token" }
    $env:GOOGLE_OAUTH_ACCESS_TOKEN = $token
    Write-Host "Authenticated. Token set for Terraform."
}
catch {
    Write-Host "Not authenticated. Logging in..."
    & $gcloud auth login
    & $gcloud config set project $PROJECT_ID
    $env:GOOGLE_OAUTH_ACCESS_TOKEN = (& $gcloud auth print-access-token)
}

# 2. Set Terraform Variables via Environment (Avoids quoting issues)
$env:TF_VAR_project_id = $PROJECT_ID
$env:TF_VAR_region = $REGION
$env:TF_VAR_gemini_api_key = $env:GEMINI_API_KEY
$env:TF_VAR_linkedin_access_token = $env:LINKEDIN_ACCESS_TOKEN
$env:TF_VAR_service_account_email = "mlops-sa@$PROJECT_ID.iam.gserviceaccount.com"

# 3. Terraform Init & Artifact Registry
Write-Host "Setting up Infrastructure (Terraform)..."
Set-Location "terraform"

if (-not (Test-Path ".terraform")) {
    terraform init
}

# Apply Resource for Artifact Registry first
Write-Host "Creating Artifact Registry..."
terraform apply -target="google_artifact_registry_repository.docker_repo" -auto-approve

Set-Location ..

# 4. Docker Build & Push
Write-Host "Checking Docker..."
try {
    docker info | Out-Null
    Write-Host "Docker is running."
    
    Write-Host "Building and Pushing Docker Image..."
    $IMAGE_URI = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/mlops-pipeline:$IMAGE_TAG"
    
    # Configure Docker auth
    & $gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet
    
    docker build -t $IMAGE_URI .
    if ($LASTEXITCODE -eq 0) {
        docker push $IMAGE_URI
    }
    else {
        throw "Docker build failed."
    }
}
catch {
    Write-Warning "Docker check failed or Docker build failed. Ensure Docker Desktop is running."
    Write-Warning "Skipping Cloud Run deployment as image push is required."
    exit 1
}

# 5. Full Deploy
Write-Host "Deploying Cloud Run Service..."
Set-Location "terraform"

terraform apply -auto-approve

# 6. Output
$SERVICE_URL = terraform output -raw service_url
Write-Host "Deployment Complete!"
Write-Host "Service URL: $SERVICE_URL"
