# twitter_sentiment_analysis

Small tweet user sentiment analysis project

![alt process](https://github.com/Kyytox/twitter_sentiment_analysis/blob/master/ressources/media/whiteboard_process_data.png)

## Install

1. Clone the project
2. Create Python Environement in base directory

```
python -m venv venv
source venv/bin/activate
```

3. Install requirements.txt

```
pip install -r requirements.txt
```

4. Install Airflow
   U can go to [Airflow Quickstart ](https://airflow.apache.org/docs/apache-airflow/stable/start.html)

define AIRFLOW_HOME 'twitter_sentiment_analysis/airflow'

```
export AIRFLOW_HOME="YOUR_PATH"
```

install airflow

```
AIRFLOW_VERSION=2.6.3

# Extract the version of Python you have installed. If you're currently using Python 3.11 you may want to set this manually as noted above, Python 3.11 is not yet supported.
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example this would install 2.6.3 with python 3.7: https://raw.githubusercontent.com/apache/airflow/constraints-2.6.3/constraints-3.7.txt

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

```

Launch Airflow

```
airflow standalone
```

## Setup

1. Setup .env file in base directory (create it)

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
# A data_to_inst.parquet file was created with all the tweets that I was able to recover
# 207613 tweets ago
# For model training, the NUMBER_DATA_TRAIN parameter allows you to choose the number of tweets to use for treatment

# If you put the line in the comments, all the tweets will be used and treated by the ML (207613 tweets)
# If you put a number, for example 1000, the first 1000 tweets of the data_to_inst.parquet file will be used and treated by the process

NUMBER_DATA_TRAIN = 1000
```

## Lauch

1. Launch Airflow

```
airflow standalone
```

❗⚠ before Launch Streamlit, you need to launch the airflow DAG "twitter_sentiment_analysis" and wait the end of the process, because the streamlit app use the data of file Gold/tweets_transform.parquet/ in AWS S3❗⚠

2. Launch Streamlit

```
streamlit run streamlit/Home.py
```
