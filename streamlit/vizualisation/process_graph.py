
import streamlit as st
import pandas as pd


# number of tweets by sentiments
def get_nb_tweets_sent(df):
    sentiments = ["positive", "negative", "neutral"]
    data_dict = {"sentiment": sentiments, "nb_tweets": [df.loc[df['sentiment'] == sent].shape[0] for sent in sentiments]}
    return data_dict


# get sum of interactions by sentiments (retweets, replies, quotes, likes) on random tweets
def get_data_interactions(df):

    # get number tweets by sentiments
    lst_nb_tweets_sent = get_nb_tweets_sent(df)
    min_value_nb_tweets = min(lst_nb_tweets_sent['nb_tweets'])

    # get random tweets by sentiments
    df_data_random = df.sample(n=min_value_nb_tweets)

    st.write(f'{min_value_nb_tweets} tweets analyzed')
    st.info('This corresponds to the number of tweets by the smallest feelings (ex: 1850 positive tweets, 1600 negatives, 1,300 neutral => we recover the number 1300 and we are looking for 1300 random tweets of each feeling, to have a gal tweets to Analyser )', icon="ℹ️")

    # select columns to create new dataframe 
    df_data_random = df_data_random[['sentiment', 'retweet_count', 'reply_count', 'like_count', 'quote_count']]

    # group by sentiment and sum interactions
    df_data_interac = df_data_random.groupby('sentiment').sum().reset_index()
    df_data_interac = df_data_interac.rename(columns={'retweet_count': 'retweets', 
                                                    'reply_count': 'replies', 
                                                    'like_count': 'likes', 
                                                    'quote_count': 'quotes'})


    # create a new dataframe with 3 columns (interactions, sentiment, count)
    df_data_interac = df_data_interac.melt(id_vars=['sentiment'], value_vars=['retweets', 'replies', 'quotes', "likes"], var_name='interactions', value_name='count')

    return df_data_interac