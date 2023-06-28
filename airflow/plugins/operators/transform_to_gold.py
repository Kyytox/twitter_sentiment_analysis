# Import libraries
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
import pandas as pd
import numpy as np
import sys
from pathlib import Path


# Utils
sys.path.append(str(Path(__file__).parent.parent))
from aws.aws_utils import get_file_aws, get_partitionned_file_aws


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
# path = f"./cardiffnlp/twitter-roberta-base-sentiment-latest"
# MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"
path = f"./cardiffnlp/twitter-xlm-roberta-base-sentiment"


tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
# tokenizer.save_pretrained(MODEL)
# config.save_pretrained(MODEL)

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
# model.save_pretrained(MODEL)



# Detect sentiment of text with model
def detect_sentiment(row):
    # detect Text sentiment
    encoded_input = tokenizer(row["text_tweet"], return_tensors="pt")
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




# Process sentiment of DataFrame
def silver_to_gold(df):
    df_sentiment = df.apply(detect_sentiment, axis=1)

    # merge df and df_sentiment by id_tweet
    df = pd.merge(df, df_sentiment, on="id_tweet")

    # define new column order
    new_order = [
        "name_user",
        "id_user",
        "id_tweet",
        "date_tweet",
        "sentiment",
        "score",
        "text_tweet",
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

    return df



# get Silver data from AWS S3
df = get_partitionned_file_aws("Silver/tweets_silver.parquet")

print(df.shape)



# # process sentiment
# df = silver_to_gold(df)

# print(df.head())

# # send to AWS S3
# df.to_parquet("Silver/tweets_collect_1618590199.parquet")
# print("Number of tweets :", len(df))