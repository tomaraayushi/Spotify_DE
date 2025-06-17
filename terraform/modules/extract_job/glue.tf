# "aws_secretmanager"
data "aws_secretsmanager_secret" "spotify_credentials" {
  arn = "arn:aws:secretsmanager:us-east-1:560154796930:secret:spotify/api/credentials-MJ34vj"
}

data "aws_secretsmanager_secret_version" "current" {
  secret_id = data.aws_secretsmanager_secret.spotify_credentials.id
}

# Resource "aws_glue_job" "spotify_api__ingestion_etl_job"
resource "aws_glue_job" "spotify_api_ingestion_etl_job" {
  name         = "${var.project}-api-extract-job"
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "4.0"

  command {
    name            = "glueetl"
    # Set the value of scripts_bucket and `"spotify-api-extract-job.py"` for the script object key
    script_location = "s3://${var.scripts_bucket}/spotify_api_extract_job.py"
    python_version  = 3
  }

  # Set the arguments in the `default_arguments` configuration parameter
  default_arguments = {
    "--enable-job-insights" = "true"
    "--job-language"        = "python"
    # Credentials for access token
    "--client_id"           = jsondecode(data.aws_secretsmanager_secret_version.current.secret_string)["client_id"]
    "--client_secret"       = jsondecode(data.aws_secretsmanager_secret_version.current.secret_string)["client_secret"]
    # API endpoint for access token
    "--api_url_token"       = "https://accounts.spotify.com/api/token"
    # API endpoint for new-releases
    "--api_url_new_releases"= "https://api.spotify.com/v1/browse/new-releases"
    # API endpoint for album tracks
    "--api_url_album_tracks"= "https://api.spotify.com/v1/albums"
    # Target path
    "--target_path"         = "s3://${var.data_lake_bucket}/landing_zone/api"
  }

  # Set up the `timeout` to 5 and the number of workers to 2. The time unit here is minutes.
  timeout = 10
  number_of_workers = 2

  worker_type       = "G.1X"
}

