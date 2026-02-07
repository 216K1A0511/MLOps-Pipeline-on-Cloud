terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  # backend "gcs" {
  #   bucket = "mlops-terraform-state"
  #   prefix = "terraform/state"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Enable Required APIs (Best Practice)
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifact_registry_api" {
  service = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

# 2. Artifact Registry for Docker images
resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = "mlops-docker-repo"
  description   = "Docker repository for MLOps pipeline"
  format        = "DOCKER"
  depends_on    = [google_project_service.artifact_registry_api]
}

# 3. GCS Buckets
resource "google_storage_bucket" "data_bucket" {
  name          = "${var.project_id}-mlops-data"
  location      = var.region
  force_destroy = false
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "model_bucket" {
  name          = "${var.project_id}-mlops-models"
  location      = var.region
  force_destroy = false
  uniform_bucket_level_access = true
}

# 4. Cloud Run Service (The API/Pipeline)
resource "google_cloud_run_service" "mlops_api" {
  name     = "mlops-pipeline-api"
  location = var.region

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.docker_repo.name}/mlops-pipeline:latest"
        
        resources {
          limits = {
            cpu    = "1000m"
            memory = "512Mi"
          }
        }
        
        env {
          name = "GEMINI_API_KEY"
          value = var.gemini_api_key
        }
        
        env {
            name = "LINKEDIN_ACCESS_TOKEN"
            value = var.linkedin_access_token
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.run_api]
}

# Allow unauthenticated access to the API (Optional - specific for portfolio demo)
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.mlops_api.location
  project     = google_cloud_run_service.mlops_api.project
  service     = google_cloud_run_service.mlops_api.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

# 5. Cloud Scheduler Job (Runs daily at 9 AM)
resource "google_project_service" "scheduler_api" {
  service            = "cloudscheduler.googleapis.com"
  disable_on_destroy = false
}

resource "google_service_account" "scheduler_sa" {
  account_id   = "scheduler-sa"
  display_name = "Cloud Scheduler Service Account"
}

resource "google_cloud_run_service_iam_member" "scheduler_invoker" {
  location = google_cloud_run_service.mlops_api.location
  project  = google_cloud_run_service.mlops_api.project
  service  = google_cloud_run_service.mlops_api.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler_sa.email}"
}

resource "google_cloud_scheduler_job" "daily_pipeline_job" {
  name             = "daily-mlops-pipeline-job"
  description      = "Triggers the MLOps pipeline every weekday at 9 AM"
  schedule         = "0 9 * * 1-5" # At 09:00 on every day-of-week from Monday through Friday.
  time_zone        = "America/Los_Angeles"
  attempt_deadline = "320s"

  http_target {
    http_method = "POST"
    uri         = "${google_cloud_run_service.mlops_api.status[0].url}/predict" # Assuming hitting predict endpoint to trigger logic or a specific '/run' endpoint
    
    body = base64encode("{\"features\": {\"trigger\": \"scheduled\"}}")
    headers = {
        "Content-Type" = "application/json"
    }

    oidc_token {
      service_account_email = google_service_account.scheduler_sa.email
    }
  }

  depends_on = [google_project_service.scheduler_api]
}

# 6. Output URL
output "service_url" {
  value = google_cloud_run_service.mlops_api.status[0].url
}