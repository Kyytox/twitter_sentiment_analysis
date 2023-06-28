import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import sys
from pathlib import Path


# Utils
sys.path.append(str(Path(__file__).parent.parent))
from aws.aws_utils import get_file_aws, send_to_aws_partition



# Format tweets for use in model
# remove specific caract usefull for help IA
def format_text(text):
    # text = text.lower()

    # remove special characters
    text = text.replace('\n', ' ').replace('\r', '')

    # remove @user and http links
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)

    return " ".join(new_text)




# create Silver Table
def transform_to_silver():

    # get history_tech from AWS S3
    df_history_tech = get_file_aws("history_tech.parquet")

    # get last timestamp_last_update
    timestamp = df_history_tech['timestamp_last_update'].max()

    # get parquet file from AWS S3
    df_silver = get_file_aws(f"Bronze/tweets_collect_{timestamp}.parquet")

    # Replace column name text_tweet by text_formatted_tweet
    df_silver.rename(columns={'text_tweet': 'text_formatted_tweet'}, inplace=True)

    # format text for best detection by IA
    df_silver['text_formatted_tweet'] = df_silver['text_formatted_tweet'].apply(lambda x: format_text(x))

    # Send df to AWS S3
    send_to_aws_partition(df_silver)



