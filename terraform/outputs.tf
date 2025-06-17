output "project" {
  value = var.project
}

# Extract module
output "glue_extract_job_name" {
  value = module.extract_job.glue_job_name
}

output "glue_extract_job_arn" {
  value = module.extract_job.glue_job_arn
}

output "glue_extract_role_arn" {
  value = module.extract_job.glue_role_arn
}

output "glue_role_arn" {
  value = module.extract_job.glue_role_arn
}

output "region" {
  value = var.region
}
