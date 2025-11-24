terraform {
  required_providers {
    fmc = {
      source  = "CiscoDevNet/fmc"
      version = "2.0.0-rc8"
    }
  }
}

provider "fmc" {
  url      = ""
  username = ""
  password = ""
}

module "nac-fmc" {
  source  = "netascode/nac-fmc/fmc"
  version = "0.1.0"
  yaml_directories = ["data"]
}
