variable "github_organization" {
  type = "string"
}

variable "repo" {
  type = "string"
}

variable "repo_user" {}

variable "tfe_org" {}

variable "atlas_token" {}

variable "config" {
  default = "~/.terraformrc"
}

variable "tfe_api" {
  default = "app.terraform.io"
  
}
