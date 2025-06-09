variable "project"{
    type = string
    description = "Project name"
}

variable "region" {
    type = string
    description = "AWS Region"
}

variable "public_subnet_a_id" {
    type = string
    description = "Private subnet A ID"
}

variable "data_lake_bucket" {
    type = string
    description = "Data Lake Bucket Name"
}

variable "scripts_bucket" {
    type = string
    description = "Data Lake Bucket Name"
}

