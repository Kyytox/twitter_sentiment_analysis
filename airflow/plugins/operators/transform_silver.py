import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


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
def create_silver_table(df):

    # Replace column name text_tweet by text_formatted_tweet
    df.rename(columns={'text_tweet': 'text_formatted_tweet'}, inplace=True)

    # format text for best detection by IA
    df['text_formatted_tweet'] = df['text_formatted_tweet'].apply(
        lambda x: format_text(x))

    df['date_tweet'].dt.tz_localize(None)

    # Format date_tweet (YYYY-MM-DD HH:MM:SS)
    df['date_tweet'] = df['date_tweet'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df
