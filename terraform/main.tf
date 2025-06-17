module "extract_job" {
    source = "./modules/extract_job"

    project = var.project
    region = var.region
    data_lake_bucket = var.data_lake_bucket
    scripts_bucket = var.scripts_bucket

}

