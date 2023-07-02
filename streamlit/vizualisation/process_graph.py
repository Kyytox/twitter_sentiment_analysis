
import streamlit as st
import pandas as pd

# sentiments = ['Positive','Neutral','Negative']
sentiments = ['Negative','Neutral','Positive']

# number of tweets by sentiments
def get_nb_tweets_sent(df):
    data_dict = {"sentiment": [], "nb_tweets": []}

    for sent in sentiments:
        data_dict["sentiment"].append(sent)
        data_dict["nb_tweets"].append(df.loc[df['sentiment'] == sent].shape[0])
    return data_dict


def get_data_interactions(df):
    # bar charts repartition interactions in sentiments
    lst_nb_tweets_sent = get_nb_tweets_sent(df)
    min_value_nb_tweets = min(lst_nb_tweets_sent['nb_tweets'])

    if st.button('Refresh'):
        # collect x random lines 
        df_data_random = df_sample = df.sample(n=min_value_nb_tweets)
    else:
        df_data_random = df_sample = df.sample(n=min_value_nb_tweets)

    st.write(f'{min_value_nb_tweets} tweets analysés')
    st.info('Cela correspond au nombre de tweets par sentiments le plus petit (ex: 1850 tweets Positifs, 1600 Négatifs, 1300 Neutres => on récupère le nombre 1300 et on cherche 1300 tweets aléatoires de chaque sentiment, pour avoir un nombre gal de tweets à anlyser )', icon="ℹ️")


    # select column for create new dataframe 
    df_new_struct = df_data_random[['sentiment', 'retweet_count', 'reply_count', 'like_count', 'quote_count']]

    # # group by interactions
    df_data_interac = df_new_struct.groupby('sentiment').sum()


    # create a new dataframe with 3 column (interactions , sentiment, count)
    df_data_bar_interac = pd.DataFrame(columns = ["interactions", "sentiment", "count"])
    for sent in sentiments:
        for x in df_data_interac.loc[df_data_interac.index == sent]:
            new_row = {'interactions': x.replace('_count', ''), 'sentiment': sent, 'count': df_data_interac[x].loc[df_data_interac.index == sent].values[0]}
            df_data_bar_interac = df_data_bar_interac.append(new_row, ignore_index=True)

    return df_data_bar_interac