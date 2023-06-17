# librairies
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import tweepy
import dotenv
import os
from time import perf_counter
import sys

# Utils
sys.path.append(str(Path(__file__).parent.parent))
from aws.aws_utils import get_file_aws, send_to_aws


# load env variables
dotenv.load_dotenv()


# Initialization Tweepy for use Twitter APi v2
def init_tweepy():
    # return tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"))
    return tweepy.Client( bearer_token=os.getenv("ACCESS_TOKEN"), 
                consumer_key=os.getenv("CONSUMER_KEY"), 
                consumer_secret=os.getenv("CONSUMER_SECRET"), 
                access_token=os.getenv("ACCESS_TOKEN"), 
                access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
                )

# get tweets
def get_tweets():
    print('os.dotenv : ', os.getenv("BEARER_TOKEN"))
    # user perf_counter
    t1_start = perf_counter()

    # get history_tech from AWS S3
    df_history_tech = get_file_aws("history_tech.parquet")

    # convert timestamp_last_update to int
    df_history_tech['timestamp_last_update'] = df_history_tech['timestamp_last_update'].astype(int)

    # create dataFrame for append tweets
    df_bronze = pd.DataFrame(
        columns=['id_user', 'name_user', 'date_tweet', 'id_tweet',
                'text_tweet',
                'nb_interactions', 'retweet_count',
                'reply_count', 'like_count', 'quote_count'])
    
    # browse df
    for key, df_user in df_history_tech.groupby('id_user'):
        print("key : ", key)
        print("df_user : ", df_user['timestamp_last_update'].dtypes)
        
        # get infos user, last update
        last_update = df_user.loc[df_user['timestamp_last_update'].idxmax()]
        print("get tweets for user : ", last_update['name_user'], " id : ", last_update['id_user'], " since id : ", last_update['last_id_tweet'])

        # init tweepy
        # client = init_tweepy()
        client = tweepy.Client(bearer_token=os.getenv("ACCESS_TOKEN"),
                            # consumer_key=os.getenv("CONSUMER_KEY"),
                            # consumer_secret=os.getenv("CONSUMER_SECRET"), 
                            # access_token=os.getenv("ACCESS_TOKEN"),
                            # access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
                            )

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

                            df_bronze = pd.concat([df_bronze, pd.DataFrame(new_row, index=[0])],
                                                ignore_index=True)

    t1_stop = perf_counter()
    print("Time process :", t1_stop - t1_start)
    print("Number of tweets :", len(df_bronze))

    # create timestamp for file name
    timestamp = str(round(datetime.now().timestamp()))

    # Send df_bronze to AWS S3
    send_to_aws(df_bronze, f"Bronze/tweets_collect_{timestamp}.parquet")
    # return df_bronze
