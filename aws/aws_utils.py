
# Aws
import boto3
import awswrangler as wr

# lib
import pandas as pd
import dotenv
import os
import io


# load env variables
dotenv.load_dotenv()


# Crédentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")



# Create S3 client
def connect_aws():
    # create S3 client
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                    region_name=AWS_REGION)

    return s3


# get file from AWS S3
def get_file_aws(key_file):
    print("-------------get file from aws-----------------")

    # create S3 client
    s3 = connect_aws()


    # get parquet from S3
    parquet_object = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=key_file)[
        'Body'].read()
    parquet_buffer = io.BytesIO(parquet_object)

    # read parquet buffer
    df = pd.read_parquet(parquet_buffer)

    return df


# send parquet to AWS S3
def send_to_aws(file_path, file_name):
    print("-----------------send file to aws-----------------")

    # create S3 client
    s3 = connect_aws()

    # upload file to S3
    s3.upload_file(file_path, AWS_BUCKET_NAME, file_name)



# send partitionned parquet to AWS S3
def send_to_aws_partition(df):
    print("-----------------send to aws partition-----------------")

    bucket = os.getenv("AWS_BUCKET_NAME")
    path_file = f"s3://{bucket}/Silver/tweets_silver.parquet"

    wr.s3.to_parquet(df,
                    path_file,
                    partition_cols=['id_user'],
                    dataset=True,
                    mode="append",
                    compression='snappy')
