variable "project" {
    type = string
    description = "Project name"
}
variable "region" {
  type        = string
  description = "AWS region"
}

# variable "vpc_id" {
#   type        = string
#   description = "VPC ID"
# }

# variable "public_subnet_a_id" {
#   type        = string
#   description = "Public subnet A ID"
# }
variable "data_lake_bucket" {
  type        = string
  description = "Data lake bucket name"
}

variable "scripts_bucket" {
  type        = string
  description = "Glue scripts bucket name"
}

# variable "new_releases_table" {
#   type        = string
#   description = "Table to store new releases data"
#   sensitive   = true
# }

# variable "albums_table" {
#   type        = string
#   description = "Table to store albums tracks data"
#   sensitive   = true
# }

