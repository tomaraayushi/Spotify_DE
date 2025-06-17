output "glue_job_name" {
  description = "Name of the created Glue job"
  value       = aws_glue_job.spotify_api_ingestion_etl_job.name
}

output "glue_job_arn" {
  description = "ARN of the created Glue job"
  value       = aws_glue_job.spotify_api_ingestion_etl_job.arn
}

output "glue_role_arn" {
  description = "ARN of the IAM role used by the Glue job"
  value       = aws_iam_role.glue_role.arn
}

