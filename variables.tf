variable "github_organization" {
  type = "string"
}

variable "repo" {
  type = "string"
}

variable "oauth_token" {
  type = "string"
}

variable "tfe_org" {
  type = "string"
  description = "Name of TFE Organization"
}

variable "tfe_token" {
  type = "string"
  description = "TFE User Token"
}


variable "config" {
  default = "~/.terraformrc"
}

variable "tfe_api" {
  default = "app.terraform.io"
  
}
