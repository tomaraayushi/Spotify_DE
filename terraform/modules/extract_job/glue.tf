# Complete the resource `"aws_glue_job" "api_new_releases_ingestion_etl_job"`
resource "aws_glue_job" "api_new_releases_ingestion_etl_job" {
  name         = "${var.project}-api-new-releases-extract-job"
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "4.0"

  command {
    name            = "glueetl"
    # Set the value of scripts_bucket and `"de-c4w4a1-api-extract-job.py"` for the script object key
    script_location = "s3://${var.scripts_bucket}/spotify-api-extract-job.py"
    python_version  = 3
  }

  # Set the arguments in the `default_arguments` configuration parameter
  default_arguments = {
    "--enable-job-insights" = "true"
    "--job-language"        = "python"
    # Set `"--api_start_date"` to `"2020-01-01"`
    # "--api_start_date"      = "2020-01-01"
    # Set `"--api_end_date"` to `"2020-01-31"`
    # "--api_end_date"        = "2020-01-31"
    # Replace the placeholder <API-ENDPOINT> with the value from the CloudFormation outputs
    "--api_url"             = "<API-ENDPOINT>"
    # Notice the target path. This line of the code code is complete - no changes are required
    "--target_path"         = "s3://${var.data_lake_bucket}/landing_zone/api/new_releases"
  }

  # Set up the `timeout` to 5 and the number of workers to 2. The time unit here is minutes.
  timeout = 5
  number_of_workers = 2

  worker_type       = "G.1X"
}

# Complete the resource `"aws_glue_job" "api_albums_tracks_ingestion_etl_job"`
resource "aws_glue_job" "api_albums_tracks_ingestion_etl_job" {
  name         = "${var.project}-api-albums-tracks-extract-job"
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "4.0"

  command {
    name            = "glueetl"
    # Set the value of scripts_bucket and `"de-c4w4a1-api-extract-job.py"` for the script object key
    script_location = "s3://${var.scripts_bucket}/spotify-api-extract-job.py"
    python_version  = 3
  }

  # Set the arguments in the `default_arguments` configuration parameter
  default_arguments = {
    "--enable-job-insights" = "true"
    "--job-language"        = "python"
    # Set `"--api_start_date"` to `"2020-01-01"`
    # "--api_start_date"      = "2020-01-01"
    # Set `"--api_end_date"` to `"2020-01-31"`
    # "--api_end_date"        = "2020-01-31"
    # Replace the placeholder <API-ENDPOINT> with the value from the CloudFormation outputs
    "--api_url"             = "<API-ENDPOINT>"
    # Notice the target path. This line of the code code is complete - no changes are required
    "--target_path"         = "s3://${var.data_lake_bucket}/landing_zone/api/albums_tracks"
  }

  # Set up the `timeout` to 5 and the number of workers to 2. The time unit here is minutes.
  timeout = 5
  number_of_workers = 2

  worker_type       = "G.1X"
}