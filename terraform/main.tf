module "extract_job" {
    source = ".modules/extract_job"

    project = var.project
    region = var.region
    public_subnet_a_id = var.public_subnet_a_id
    data_lake_bucket = var.data_lake_bucket
    scripts_bucket = var.scripts_bucket

}

