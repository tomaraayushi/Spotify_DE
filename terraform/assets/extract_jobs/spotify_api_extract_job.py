import datetime as dt
import requests
import json
import os
import sys
import boto3

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import GetResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession, SparkSQL
from pyspark.sql.functions import col
from typing import Dict, Any
from dotenv import load_dotenv

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
    return {"Authentication": f"Bearer {access_token}"}


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
            new_released_data.extend(response_json.get('items'))
            request_url = response_json.get('next')

        return new_released_data

    except Exception as err:
        print(f"Error: {err}")
        return []
    
# Endpoint-Albums Tracks
def get_paginated_albums_tracks(base_url:str, access_token:str, album_id:str)-> list:
    headers = get_auth_header(access_token)
    request_url = base_url
    album_data = []

    try:
        while request_url:
            response = requests.get(url=request_url, headers=headers, id=album_id)
            response.raise_for_status()
            response_json = response.json()
            album_data.extend(response_json.get('items'))
            request_url = response_json.get('next')

        return album_data

    except Exception as err:
        print(f"Error: {err}")
        return []
    
# Main Job Execution





    

        























CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

URL_TOKEN = "https://accounts.spotify.com/api/token"
URL_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
URL_ALBUMS_TRACKS = "https://api.spotify.com/v1/albums"








