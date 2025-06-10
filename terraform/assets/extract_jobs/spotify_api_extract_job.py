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


from dotenv import load_dotenv
from spotify_api_endpoints import (
    get_paginated_new_releases,
    get_paginated_albums_tracks
)

from authentication import get_token 

load_dotenv('./src/env', override=True)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

URL_TOKEN = "https://accounts.spotify.com/api/token"
URL_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
URL_ALBUMS_TRACKS = "https://api.spotify.com/v1/albums"








