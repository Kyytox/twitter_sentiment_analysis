
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
    s3 = boto3.client('s3', 
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                    region_name=AWS_REGION)

    return s3


# get file from AWS S3
def get_file_aws(key_file):
    print("----------get file from aws----------")

    # create S3 client
    s3 = connect_aws()

    # get parquet from S3
    parquet_object = s3.get_object(Bucket=AWS_BUCKET_NAME, Key=key_file)['Body'].read()
    parquet_buffer = io.BytesIO(parquet_object)

    # read parquet buffer
    df = pd.read_parquet(parquet_buffer)

    return df



def get_partitionned_file_aws(key_file):

    # create S3 client
    s3 = connect_aws()

    # get parquet from S3
    df = wr.s3.read_parquet(path=f"s3://{AWS_BUCKET_NAME}/{key_file}")

    return df




# check if file exist in AWS S3
def check_file_aws(key_file):
    print("----------check file in aws----------")

    # create S3 client
    s3 = connect_aws()

    # get list object in bucket
    response = s3.list_objects_v2(Bucket=AWS_BUCKET_NAME)

    # check if file exist
    if 'Contents' in response.keys():
        for file in response['Contents']:
            if file['Key'] == key_file:
                return True
    else:
        return False



# send parquet to AWS S3
def send_to_aws(df, file_name):
    print("----------send to aws----------")

    # create S3 client
    s3 = connect_aws()

    # create path file
    path_file = f"s3://{AWS_BUCKET_NAME}/{file_name}"

    # upload file to S3
    wr.s3.to_parquet(
        df=df,
        path=path_file,
    )



# send partitionned parquet to AWS S3
def send_to_aws_partition(df):
    print("----------send partitionned to aws----------")

    # get bucket name
    path_file = f"s3://{AWS_BUCKET_NAME}/Gold/tweets_transform.parquet"

    # send to aws
    wr.s3.to_parquet(df,
                    path_file,
                    partition_cols=['id_user'],
                    dataset=True,
                    mode="append",
                    compression='snappy')
