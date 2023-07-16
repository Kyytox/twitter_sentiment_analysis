
Small tweet user sentiment and interactions analysis project.


<br/>

# Table of Contents

- [Architecture](#architecture)
- [Process](#process)
    - [1. Check data_history](#1-check-data_history)
    - [2. Extract data](#2-extract-data)
    - [3. Transform data](#3-transform-data)
- [Visualisation](#visualisation)
    - [1. Sentiment Analysis](#1-sentiment-analysis)
    - [2. Interactions](#2-interactions)
    - [3. Frequent Words](#3-frequent-words)
- [Install](#install)
- [Setup](#setup)
- [Launch](#launch)

<br/>

---
# Architecture

![alt process](https://github.com/Kyytox/twitter_sentiment_analysis/blob/master/ressources/media/whiteboard_process_data.png)

- **Airflow**: Process orchestration
- **AWS S3**: Data storage
- **Streamlit**: Display of results
- **Python**: Data processing
- **.Parquet**: Data format
- **ML Model**: [cardiffnlp/twitter-xlm-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment)


<br/>

---
# Process

Since June 2023, Twitter has restricted access to his V2 API.
Thus, it is no longer possible to recover user tweets.

So I recovered the user tweets that I could before this date and stored them in a .parquet file.
It's with this file that I will work for the process.
You find this file in the folder **ressources/data/data_to_insert.parquet**

This file contains 207613 tweets

With Param NUMBER_DATA_TRAIN in .env file, you can choose the number of tweets extract from the data_to_insert.parquet file for the process.

❗⚠ **So Twitter API V2 is no longer used for this project.** ❗⚠ 

<br/>

## 1. Check data_history

Check if the data_history.parquet file exists in AWS S3.
If not, a new file is created with template **ressources/data/data_history.xlsx**

This file contains the tweets already treated by the process.

| Column | Type |
|--------|------|
| date_last_update | object |
| timestamp_last_update | int64 |
| id_user | int64 |
| name_user | object |
| last_id_tweet | int64 |
| date_tweet | datetime64[ns] |

<br/>

## 2. Extract data

Extract data from data_to_insert.parquet file
According to the NUMBER_DATA_TRAIN parameter, and df_data_history, the process will extract the tweets to be treated.

The new data is stored in **Bronze/tweets_collect_{timestamp}.parquet** in AWS S3

| Column | Type |
|--------|------|
| id_user | int64 |
| name_user | object |
| date_tweet | datetime64[ns] |
| id_tweet | int64 |
| text_tweet | object |
| nb_interactions | int64 |
| retweet_count | int64 |
| reply_count | int64 |
| like_count | int64 |
| quote_count | int64 |

<br/>

## 3. Transform data

Get Last file in Bronze folder in AWS S3

Load the model [cardiffnlp/twitter-xlm-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment)

Format the text of the tweets
Predict the sentiment of the tweets

The new data is stored in **Gold/tweets_transform.parquet** in AWS S3
The parquet file is partitioned by id_user


| Column | Type |
|--------|------|
| id_user | int64 |
| name_user | object |
| date_tweet | datetime64[ns] |
| id_tweet | int64 |
| text_formatted_tweet | object |
| nb_interactions | int64 |
| retweet_count | int64 |
| reply_count | int64 |
| like_count | int64 |
| quote_count | int64 |
| sentiment | object |
| score | float64 |
| negative | float64 |
| neutral | float64 |
| positive | float64 |


<br/>

---
# Visualisation

Streamlit is used to display the results of the process.


## 1. Sentiment

Display the sentiment analysis of the tweets of the user selected in the dropdown list.

- Pie chart
	- Distribution of the sentiment of the tweets

- Bar chart
	- Number of tweets by sentiment
	- Number of tweets by sentiment and by month
	- Number of tweets by sentiment and by day of month

- Line chart
	- Mean score of the sentiment of the tweets (multitple interval of time)

- Box chart
	- Demonstrating the locatity, spread and skewness of the sentiment

<br/>

## 2. Interactions

Display the interactions of the tweets of the user selected in the dropdown list.

- Line chart
	- Number of total interactions (multitple interval of time)

- Bar chart
	- Number of interactions by type (retweet, reply, like, quote)

- Pie chart
	- Distribution of the interactions by type and by sentiment

<br/>

## 3. Frequent Words

Display the most frequent words of the tweets of the user selected in the dropdown list.

- Wordcloud
	- Most 200 frequent words of the tweets



<br/>

---
# Install

#### 1. Clone the project
#### 2. Create Python Environement in base directory

```
python -m venv venv
source venv/bin/activate
```


#### 3. Install requirements.txt
```
pip install -r requirements.txt
```


#### 4. Install Airflow

U can go to [Airflow Quickstart ](https://airflow.apache.org/docs/apache-airflow/stable/start.html)

define AIRFLOW_HOME 'twitter_sentiment_analysis/airflow'
```
export AIRFLOW_HOME="YOUR_PATH"
```

```
AIRFLOW_VERSION=2.6.3

# Extract the version of Python you have installed. If you're currently using Python 3.11 you may want to set this manually as noted above, Python 3.11 is not yet supported.
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.6.3 with python 3.7: https://raw.githubusercontent.com/apache/airflow/constraints-2.6.3/constraints-3.7.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

<br/>

---
# Setup

#### 1. Setup .env file in base directory (create it)
```
# ------------- Credentials -------------
# AWS Credentials
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_BUCKET_NAME = ''
AWS_REGION = ''

# token Twitter API v2
BEARER_TOKEN = ''


# ------------- Param Process -------------
# Parameters for treatment of data
# In June 2023, Twitter restricted access to API V2
# So we could no longer recover the tweets from the users
# A data_to_insert.parquet file was created with all the tweets that I was able to recover
# 207613 tweets ago
# For model training, the NUMBER_DATA_TRAIN parameter allows you to choose the number of tweets to use for treatment

# If you put the line in the comments, all the tweets will be used and treated by the ML (207613 tweets)
# If you put a number, for example 1000, the first 1000 tweets of the data_to_insert.parquet file will be used and treated by the process

NUMBER_DATA_TRAIN = 1000
```


#### 2. Aiflow.cfg

In file airflow/airflow.cfg remove the exemple dags
```
# Line 66
load_examples = False
```

<br/>

---
# Launch

❗⚠ before Launch Streamlit, you need to launch the airflow DAG "twitter_sentiment_analysis" and wait the end of the process, because the streamlit app use the data of file **Gold/tweets_transform.parquet/** in AWS S3❗⚠

<br/>

#### 1. Airflow
```
airflow standalone
```
<br/>

#### 2. Streamlit
```
streamlit run streamlit/Home.py
```










