output "project" {
  value = var.project
}

# Extract module
output "glue_api_new_releases_extract_job" {
  value = module.extract_job.glue_api_new_releases_extract_job
}

output "glue_albums_tracks_extract_job" {
  value = module.extract_job.glue_albums_tracks_extract_job
}

output "glue_role_arn" {
  value = module.extract_job.glue_role_arn
}