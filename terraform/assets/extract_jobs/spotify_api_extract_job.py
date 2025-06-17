import requests
import json
import os
import sys
import boto3
from datetime import datetime

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from typing import Dict, Any, List


# Authentication function
def get_token(client_id:str, client_secret:str, url:str) -> Dict[Any, Any]:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type" : "client_credentials",
        "client_id" : client_id,
        "client_secret": client_secret
    }

    try:
        response = requests.post(url = url , headers=headers, data=payload)
        response.raise_for_status()

        response_json = response.json()
        return response_json
    
    except Exception as err:
        print(f"Error: {err}")
        return {}
    
# Authorization Header 
def get_auth_header(access_token:str)-> Dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}


# API Endpoints Functions
# Endpoint-New Releases
def get_paginated_new_releases(base_url: str, access_token:str)-> list:

    headers = get_auth_header(access_token)
    request_url = base_url
    new_released_data = []

    try:
        while request_url:
            response = requests.get(url=request_url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            new_released_data.extend(response_json.get('albums')['items'])
            request_url = response_json['albums'].get('next')

        return new_released_data

    except Exception as err:
        print(f"Error: {err}")
        return []
    
# Endpoint-Albums Tracks
def get_paginated_album_tracks(base_url:str, access_token:str, album_id:str)-> list:
    headers = get_auth_header(access_token)
    request_url = f"{base_url}/{album_id}/tracks"
    album_data = []

    try:
        while request_url:
            response = requests.get(url=request_url, headers=headers)
            response.raise_for_status()
            response_json = response.json()
            tracks = response_json.get('items')
            for track in tracks:
                track['album_id'] = album_id
            album_data.extend(tracks)
            request_url = response_json.get('next')

        return album_data

    except Exception as err:
        print(f"Error: {err}")
        return []
    
# Main Job Execution
def main():
    # Initialize Glue job
    args = getResolvedOptions(
        sys.argv, 
        [
            "JOB_NAME",
            "target_path",
            "client_id",
            "client_secret",
            "api_url_token",
            "api_url_new_releases",
            "api_url_album_tracks"
        ])

    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    job = Job(glueContext)
    job.init(args["JOB_NAME"], args)

    # Get API credentials from job parameters
    CLIENT_ID = args["client_id"]
    CLIENT_SECRET = args["client_secret"]

    # API URLS
    URL_TOKEN = args["api_url_token"]
    URL_NEW_RELEASES = args["api_url_new_releases"]
    URL_ALBUMS_TRACKS = args["api_url_album_tracks"]
    TARGET_PATH = args["target_path"]

    current_date = datetime.now().strftime("%Y-%m-%d")

    print(f"Starting Spotify data for extraction {current_date}")


    # Extract data 
    # 1.Get token
    token = get_token(CLIENT_ID, CLIENT_SECRET, URL_TOKEN)
    access_token = token.get('access_token')

    if not access_token:
        raise Exception("Failed to get access token")
    
    print("Access token obtained successfully")

    # 2. Get New Releases data
    print("Fetching new releases data...")
    new_released = get_paginated_new_releases(URL_NEW_RELEASES, access_token)
    print(f"Found {len(new_released)} new releases")

    # 3. Get Album Tracks data
    album_ids = [album['id'] for album in new_released]
    album_tracks = []
    for album_id in album_ids:
        tracks_data = get_paginated_album_tracks(URL_ALBUMS_TRACKS, access_token, album_id)
        album_tracks.extend(tracks_data)

    # 4.Transform data to Spark Dataframes
    # NEW RELEASES DATAFRAME
    new_released_rdd = sc.parallelize([json.dumps(record) for record in new_released])
    new_released_df = spark.read.json(new_released_rdd)

    # Metadata
    new_released_df = new_released_df.withColumn("ingest_date", lit(current_date)) \
                                   .withColumn("source", lit("spotify_api"))
    
    # Write new releases data to S3
    new_released_df.write.mode("overwrite").json(f"{TARGET_PATH}/new_releases/ingest_date={current_date}/")

    # ALBUM TRACKA DATAFRAME

    tracks_rdd = sc.parallelize([json.dumps(track) for track in album_tracks])
    tracks_df = spark.read.json(tracks_rdd) 

    # Metatdata
    tracks_df = tracks_df.withColumn("ingest_date", lit(current_date)) \
                        .withColumn("source", lit("spotify_api"))
    
    # Write tracks data to S3
    tracks_df.write.mode("overwrite").json(f"{TARGET_PATH}/tracks/ingest_date={current_date}/")

    print("Data extraction completed successfully!")

    # Commit job
    job.commit()

if __name__ == '__main__':
    main()






    










                 







    

        































