terraform {
  backend "s3" {
    bucket         = "terarform-state-spotify-at"
    key            = "spotify/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}