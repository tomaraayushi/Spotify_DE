variable "project"{
    type = string
    description = "Project name"
}

variable "environment" {
    type = string
    description = "Environment name"
    default = "dev"
}
variable "region" {
    type = string
    description = "AWS Region"
}

variable "data_lake_bucket" {
    type = string
    description = "Data Lake Bucket Name"
}

variable "scripts_bucket" {
    type = string
    description = "Scripts Bucket Name"
}

