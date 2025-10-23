terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.7.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project = var.project_name
  region  = var.region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
