# Import libraries
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
import pandas as pd
import numpy as np
import os
import dotenv

# helpers
from helpers.aws_utils import get_file_aws
from helpers.aws_utils import send_to_aws_partition


dotenv.load_dotenv()

"""
Transform data

- Get data from AWS S3 according to the last timestamp
- Format text for best detection by IA
- Detect sentiment of text with model "cardiffnlp/twitter-roberta-base-sentiment-latest"
- Send df to AWS S3 in parquet file, partitioned by id_user

"""


MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    return tokenizer, config, model



def get_data():
    # get history_tech from AWS S3
    df_history = get_file_aws("data_history.parquet")

    # get last timestamp
    timestamp = df_history['timestamp_last_update'].max()

    # get parquet file from AWS S3
    return get_file_aws(f"Bronze/tweets_collect_{timestamp}.parquet")



# Format tweets for use in model
# remove specific caract usefull for help IA
def format_text(text):

    # remove special characters
    text = text.replace('\n', ' ').replace('\r', '')

    # remove @user and http links
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)

    return " ".join(new_text)




# Detect sentiment of text with model
def detect_sentiment(row, tokenizer, config, model):
    # detect Text sentiment
    encoded_input = tokenizer(row["text_formatted_tweet"], return_tensors="pt")
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()

    # Format outup : [Negative - Neutral - Positive]
    scores = softmax(scores)

    # Collect the max score and the sentment
    ranking = np.argsort(scores)
    ranking = ranking[::-1]

    l = config.id2label[ranking[0]]
    s = scores[ranking[0]]
    st_score = np.round(float(s), 3)

    # add new row to DataFrame
    new_row = {
        "id_tweet": row["id_tweet"],
        "sentiment": l,
        "score": st_score,
        "negative": np.round(float(scores[0]), 3),
        "neutral": np.round(float(scores[1]), 3),
        "positive": np.round(float(scores[2]), 3),
    }

    return pd.Series(new_row)




def reindex_dataframe(df):

    # define new column order
    new_order = [
        "name_user",
        "id_user",
        "id_tweet",
        "date_tweet",
        "sentiment",
        "score",
        "text_formatted_tweet",
        "negative",
        "neutral",
        "positive",
        "nb_interactions",
        "retweet_count",
        "reply_count",
        "like_count",
        "quote_count",
    ]

    # reindex columns
    df = df.reindex(columns=new_order)




# main 
def transform_data():

    # load model
    tokenizer, config, model = load_model()

    # get data
    df = get_data()

    # format text
    df.rename(columns={'text_tweet': 'text_formatted_tweet'}, inplace=True)
    df["text_formatted_tweet"] = df["text_formatted_tweet"].apply(format_text)

    # detect sentiment
    df_sentiment = df.apply(detect_sentiment, axis=1, args=(tokenizer, config, model))

    # reindex df
    df = pd.merge(df, df_sentiment, on="id_tweet")

    # Send to AWS S3
    send_to_aws_partition(df, "Gold/tweets_transform.parquet")

    return df
