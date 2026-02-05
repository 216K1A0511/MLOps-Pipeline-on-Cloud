#!/bin/bash

# MLOps Pipeline Setup Script

set -e

PROJECT_ID="your-project-id"
REGION="us-central1"
SA_NAME="mlops-pipeline-sa"

echo "Setting up MLOps Pipeline on GCP..."

# Enable required APIs
gcloud services enable \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  containerregistry.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  compute.googleapis.com \
  storage.googleapis.com \
  cloudscheduler.googleapis.com

# Create service account
gcloud iam service-accounts create ${SA_NAME} \
  --display-name="MLOps Pipeline Service Account"

SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant roles
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/aiplatform.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/cloudbuild.builds.editor"

# Create buckets
gsutil mb -l ${REGION} gs://${PROJECT_ID}-mlops-data
gsutil mb -l ${REGION} gs://${PROJECT_ID}-mlops-models
gsutil mb -l ${REGION} gs://${PROJECT_ID}-pipeline-root

# Create Artifact Registry
gcloud artifacts repositories create mlops-docker-repo \
  --repository-format=docker \
  --location=${REGION} \
  --description="Docker repository for MLOps"

# Generate service account key
gcloud iam service-accounts keys create ./credentials.json \
  --iam-account=${SA_EMAIL}

echo "Setup completed!"
echo "Service Account Key saved to: ./credentials.json"
echo "Update GitHub Secrets with this key"