import json
import sys
from datetime import datetime

from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.functions import col, lit, explode, to_date


# Initialize GlueContext and Spark session
args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "catalog_database",         # Glue catalog database name
        "ingest_date",              # The date when data was ingested
        "new_releases_source_path", # Object's path in the source data lake for new-releases data
        "album_tracks_source_path"  # Object's path in the source data lake for album tracks data
        "target_bucket_path",       # Object's path in the destination data lake
        "new_releases_table",       # Name of new-releases albums table inside the Glue Catalog database
        "album_tracks_table",       # Name of tracks table inside the Glue Catalog Database
        "artists_table"             # Name of artists table inside the Glue Catalog Database
    ]

)

# Glue Job configuration to store data in Apache Iceberg format
conf = SparkConf()
conf.set(
    "spark.sql.extensions",
    "org.apache.iceberg.spark.extensions.icebergsSparkSessionExtensions",
)
conf.set(
    "spark.sql.catalog.glue_catalog",
    "org.apache.iceberg.spark.SparkCatalog",
)
conf.set(
    "spark.sql.catalog.glue_catalog.warehouse",
    f"s3://{args['target_bucket_path']}/transform_zone",
)
conf.set(
    "spark.sql.catalog.glue_catalog.catalog_impl",
    "org.apache.iceberg.aws.glue.GlueCatalog",
)
conf.set(
    "spark.sql.catalog.glue_catalog.io-impl",
    "org.apache.iceberg.aws.s3.S3.FileIO",
)


sc = SparkContext(conf=conf)
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
logger = glueContext.get_logger()

# Define S3 paths
ingestion_timestamp = args["ingest_date"]
s3_new_releases_path = args["new_releases_source_path"]
s3_album_tracks_path = args["album_tracks_source_path"]

# Read JSON data from S3
new_releases_df = spark.read.json(s3_new_releases_path)
tracks_df = spark.read.json(s3_album_tracks_path)

processing_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Transform new releases data
# Add processing timestamp data column and change the type of ingestion timestamp column 
new_releases_df = (
    new_releases_df.withColumn("ingestion_timestamp", to_date(col("ingestion_timestamp")))
    .withColumn("processing_timestamp", lit(processing_timestamp))
)

# 
