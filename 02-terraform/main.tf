terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.7.0"
    }
  }
}

provider "google" {
  project = "nytaxi-475716"
  region  = "europe-west1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "nytaxi-475716-terraform-test"
  location      = "EUROPE-WEST1"
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
