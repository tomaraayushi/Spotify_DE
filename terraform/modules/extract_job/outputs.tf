output "glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}

output "glue_api_new_releases_extract_job" {
  value = aws_glue_job.api_new_releases_ingestion_etl_job.name
}

output "glue_albums_tracks_extract_job" {
  value = aws_glue_job.api_albums_tracks_ingestion_etl_job.name
}

