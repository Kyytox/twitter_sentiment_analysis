
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Helpers
from helpers.history_utils import create_history_tech

# Operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from operators.extraction_tweets import get_tweets
from operators.transform_data import transform_data



with DAG(
    "tweets_sentiment_analysis",
    # default_args={
    #     "depends_on_past": False,
    #     "retries": 1,
    #     "retry_delay": timedelta(minutes=5),
    # },
    description="Get tweets for analysis sentiment with ML",
    # schedule='@daily',
    schedule='@once',
    start_date=datetime(2023, 6, 1),
    catchup=False,
    tags=["tweets, ML, sentiment analysis"],

) as dag:

    # display date
    start = BashOperator(
        task_id="start",
        bash_command="date",
    )

    # Task 1: check if file exists
    # if not create it with infos of history_tech.xlsx
    check_history_tech = PythonOperator(
        task_id='check_file_history_aws',
        python_callable=create_history_tech,
        op_kwargs={'key_file': "data_history.parquet"},
        dag=dag
    )

    # # Task 3: get tweets
    get_tweets = PythonOperator(
        task_id='get_tweets',
        python_callable=get_tweets,
        dag=dag
    )


    # Task 4: Detect sentiment
    transform_tweets = PythonOperator(
        task_id='transform_tweets',
        python_callable=transform_data,
        dag=dag
    )


    # Run tasks
    start >> check_history_tech >> get_tweets >> transform_tweets