# Google Cloud Platform (GCP) Setup Guide

This guide helps you create the necessary credentials to deploy your MLOps pipeline using Terraform.

## 1. Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown/selector in the top bar.
3. Click "New Project".
4. Name it (e.g., `gemini-mlops-prod`) and Note the **Project ID** (it might involve random numbers).

## 2. Enable Required APIs
Open the Cloud Shell (top right icon) or search for "APIs & Services" > "Library" and enable:
*   **Compute Engine API**
*   **Vertex AI API**
*   **Artifact Registry API**
*   **Cloud Build API**

## 3. Create a Service Account (For Terraform)
Terraform needs an identity to create buckets and registries for you.

1. Go to **IAM & Admin** > **Service Accounts**.
2. Click **Create Service Account**.
   *   **Name:** `terraform-deployer`
   *   **Description:** "Automated Infrastructure Provisioning"
3. Click **Create and Continue**.
4. **Grant Access (Roles):**
   *   Select **Basic** > **Editor** (Easiest for testing)
   *   OR for production, add specific roles: `Storage Admin`, `Vertex AI Admin`, `Artifact Registry Admin`.
5. Click **Done**.

## 4. Generate the Key File
1. Click on the newly created Service Account email (`terraform-deployer@...`).
2. Go to the **Keys** tab.
3. Click **Add Key** > **Create new key**.
4. Select **JSON** and click **Create**.
5. The file will download to your computer.

## 5. Configure Your Project
1. Rename the downloaded file to `gcp_key.json` (or similar).
2. Move it to your project folder (add it to `.gitignore` so you don't commit it!).
3. Open `terraform/terraform.tfvars` and set:
   ```hcl
   project_id            = "your-project-id-123"
   service_account_email = "terraform-deployer@your-project-id-123.iam.gserviceaccount.com"
   # You may need to update variables.tf to accept a key path if creating one locally
   ```

## 6. Run Terraform
```powershell
cd terraform
terraform init
terraform apply
```
