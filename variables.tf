variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region for resources"
  type        = string
  default     = "us-central1"
}

variable "service_account_email" {
  description = "Service Account Email for MLOps pipeline"
  type        = string
}

variable "gemini_api_key" {
  description = "Gemini API Key"
  type        = string
  sensitive   = true
}

variable "linkedin_access_token" {
  description = "LinkedIn Access Token"
  type        = string
  sensitive   = true
  default     = ""
}