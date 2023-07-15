# librairies
from pathlib import Path
from datetime import datetime
import pandas as pd
import tweepy
import dotenv
import os
import sys


PLUGIN_DIR = Path(__file__).parent.parent

# helpers
sys.path.append(str(PLUGIN_DIR))
from helpers.aws_utils import get_file_aws, send_to_aws
from helpers.history_utils import update_history_tech


# load env variables
dotenv.load_dotenv()



# fonction test for insert new data because API twitter is not free
def get_tweets():

    # get history_tech from AWS S3
    df_history = get_file_aws("data_history.parquet")

    # read parquet data_to_insert
    df_bronze = pd.read_parquet("ressources/data/data_to_insert.parquet")

    # create timestamp for file name
    timestamp = str(round(datetime.now().timestamp()))

    # Send df_bronze to AWS S3
    send_to_aws(df_bronze, f"Bronze/tweets_collect_{timestamp}.parquet")

    # update history_tech
    update_history_tech(df_history, df_bronze, timestamp)



# Initialization Tweepy for use Twitter APi v2
def init_tweepy():
    return tweepy.Client(os.getenv("BEARER_TOKEN"))



# get tweets with Tweepy 
# But API Twitter is not free now 
def get_tweets_with_tweepy():
    # init tweepy
    client = init_tweepy()

    # get history_tech from AWS S3
    df_history = get_file_aws("data_history.parquet")

    # convert timestamp_last_update to int
    df_history['timestamp_last_update'] = df_history['timestamp_last_update'].astype(int)

    # create dataFrame for append tweets
    df_bronze = pd.DataFrame(
        columns=['id_user', 'name_user', 'date_tweet', 'id_tweet',
                'text_tweet',
                'nb_interactions', 'retweet_count',
                'reply_count', 'like_count', 'quote_count'])
    
    # browse df
    for key, df_user in df_history.groupby('id_user'):        
        # get infos user, last update
        last_update = df_user.loc[df_user['timestamp_last_update'].idxmax()]


        # Retrive maximum tweets of users since id retrieve (max 3200)
        tweets = tweepy.Paginator(client.get_users_tweets,
                                last_update['id_user'],
                                since_id=last_update['last_id_tweet'],
                                tweet_fields=[
                                    'created_at', 'public_metrics',
                                    'in_reply_to_user_id', 'referenced_tweets'],
                                expansions=['author_id'],
                                # max_results=100, limit=33)
                                max_results=10, limit=3)

        # browse tweets
        for tweet in tweets:
            if tweet.data != None:
                for x in tweet.data:
                    # remove retweets and replies
                    if x.in_reply_to_user_id is None:
                        if x.referenced_tweets is None or x.referenced_tweets[0]['type'] == 'quoted':

                            # Retrieve Metrics , interactions
                            retweet_count = x.public_metrics['retweet_count']
                            reply_count = x.public_metrics['reply_count']
                            like_count = x.public_metrics['like_count']
                            quote_count = x.public_metrics['quote_count']
                            nb_inter = retweet_count + reply_count + like_count + quote_count

                            # insert in DataFrame
                            new_row = {'id_user': last_update['id_user'],
                                    'name_user': last_update['name_user'],
                                    'date_tweet': x.created_at,
                                    'id_tweet': x.id,
                                    'text_tweet': x.text,
                                    'nb_interactions': nb_inter,
                                    'retweet_count': retweet_count,
                                    'reply_count': reply_count,
                                    'like_count': like_count,
                                    'quote_count': quote_count}

                            df_bronze = pd.concat([df_bronze, pd.DataFrame(new_row, index=[0])], ignore_index=True)


    # create timestamp for file name
    timestamp = str(round(datetime.now().timestamp()))

    # Send df_bronze to AWS S3
    send_to_aws(df_bronze, f"Bronze/tweets_collect_{timestamp}.parquet")

    update_history_tech(df_history, df_bronze, timestamp)