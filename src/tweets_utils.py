# librairies
from datetime import datetime, timedelta
import pandas as pd
import tweepy
import dotenv
import os
from time import perf_counter


# Utils
from utils.aws_utils import get_file_aws

# load env variables
dotenv.load_dotenv()

# Initialization Tweepy for use Twitter APi v2
client = tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"))

# get tweets
def get_tweets(df_history_tech):
    # user perf_counter
    t1_start = perf_counter()

    # create dataFrame for append tweets
    df_bronze = pd.DataFrame(
        columns=['id_user', 'name_user', 'date_tweet', 'id_tweet',
                'text_tweet',
                'nb_interactions', 'retweet_count',
                'reply_count', 'like_count', 'quote_count'])

    # # browse df
    # for user in df_history_tech.id_user.unique():

    #     # find row with last timestamp_last_update
    #     df_user = df_history_tech[df_history_tech.id_user == user]
    #     df_user = df_user[df_user.timestamp_last_update ==
    #                     df_user.timestamp_last_update.max()]

    #     # infos user
    #     id_user = df_user.id_user.values[0]
    #     name_user = df_user.name_user.values[0]
    #     last_id_tweet = df_user.last_id_tweet.values[0]
    
    # browse df
    for df_user in df_history_tech.groupby('id_user'):
        
        last_update = df_user.loc[df_user.timestamp_last_update.idxmax()]
        id_user = last_update['id_user']
        name_user = last_update['name_user']
        last_id_tweet = last_update['last_id_tweet']

        # for tests
        # last_id_tweet = int(
        #     df_user.last_id_tweet.values[0]) - 5000 if df_user.last_id_tweet.values[0] != '1' else '1'

        print("get tweets for user : ", name_user, " id : ", id_user)

        # Retrive maximum tweets of users since id retrieve (max 3200)
        tweets = tweepy.Paginator(client.get_users_tweets,
                                id_user,
                                since_id=last_id_tweet,
                                tweet_fields=[
                                    'created_at', 'public_metrics',
                                    'in_reply_to_user_id', 'referenced_tweets'],
                                expansions=['author_id'],
                                # max_results=100, limit=33)
                                max_results=7, limit=3)

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
                            new_row = {'id_user': id_user,
                                    'name_user': name_user,
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

    return df_bronze
