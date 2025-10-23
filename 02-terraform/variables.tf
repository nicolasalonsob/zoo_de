variable "credentials" {
  description = "Project credentials"
  default     = "./keys/my-cred.json"
}

variable "project_name" {
  description = "Name of the project"
  default     = "nytaxi-475716"

}
variable "location" {
  description = "Default location"
  default     = "EUROPE-WEST1"

}
variable "region" {
  description = "Default location"
  default     = "europe-west1"


}
variable "bucket_name" {
  description = "demo-bucket"
  default     = "nytaxi-475716-terraform-test"

}
