# Airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# librairies
from datetime import datetime, timedelta



# init Airflow DAG arguments
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 6, 3, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}


# define the DAG
dag = DAG(
    dag_id='tweets_sentiment_analysis',
    default_args=default_args,
    description='Get tweets for analysis sentiment with ML',
    schedule_interval=timedelta(hours=2),
    # schedule_interval=timedelta(minutes=2),
)