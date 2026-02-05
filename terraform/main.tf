terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  backend "gcs" {
    bucket = "mlops-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# GCS Buckets
resource "google_storage_bucket" "data_bucket" {
  name          = "${var.project_id}-mlops-data"
  location      = var.region
  force_destroy = false
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_storage_bucket" "model_bucket" {
  name          = "${var.project_id}-mlops-models"
  location      = var.region
  force_destroy = false
  
  versioning {
    enabled = true
  }
}

# Artifact Registry for Docker images
resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "mlops-docker-repo"
  description   = "Docker repository for MLOps pipeline"
  format        = "DOCKER"
}

# Vertex AI Dataset
resource "google_vertex_ai_dataset" "training_data" {
  display_name        = "training-dataset"
  metadata_schema_uri = "gs://google-cloud-aiplatform/schema/dataset/metadata/tabular_1.0.0.yaml"
  region              = var.region
}

# Cloud Scheduler for automated retraining
resource "google_cloud_scheduler_job" "daily_retraining" {
  name        = "daily-ml-retraining"
  description = "Trigger daily ML model retraining"
  schedule    = "0 2 * * *"
  time_zone   = "UTC"
  
  http_target {
    http_method = "POST"
    uri         = "https://${var.region}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_id}/jobs/trigger-training:run"
    
    oauth_token {
      service_account_email = var.service_account_email
    }
  }
}

# IAM permissions
resource "google_project_iam_member" "vertex_ai_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${var.service_account_email}"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${var.service_account_email}"
}