# Deploy to Azure Container Instances (ACI)

# Ensure you are logged in: az login
# Ensure Resource Group exists: az group create --name mlops-rg --location eastus

az container create `
  --resource-group mlops-rg `
  --name gemini-mlops `
  --image 216k1a0511/gemini-mlops:latest `
  --environment-variables GEMINI_API_KEY=AIzaSyDN0Jb5jF9djDdF5Y3yqkpPvCa21VasLKw `
  --ports 8080 `
  --cpu 2 `
  --memory 4 `
  --restart-policy OnFailure

# Check status
# az container show --resource-group mlops-rg --name gemini-mlops --query instanceView.state
