
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Helpers
from helpers.history_utils import create_history_tech

# Operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from operators.extraction_tweets import get_tweets__
from operators.transform_data import transform_data



with DAG(
    "tweets_sentiment_analysis",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    # default_args={
    #     "depends_on_past": False,
    #     "email": ["airflow@example.com"],
    #     "email_on_failure": False,
    #     "email_on_retry": False,
    #     "retries": 1,
    #     "retry_delay": timedelta(minutes=2),
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

    start.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
    )

    # Task 1: check if file exists
    # if not create it with infos of history_tech.xlsx
    check_history_tech = PythonOperator(
        task_id='check_file_history_aws',
        python_callable=create_history_tech,
        op_kwargs={'key_file': "history_tech.parquet"},
        show_return_value_in_logs=True,
        dag=dag
    )

    # # Task 3: get tweets
    get_tweets = PythonOperator(
        task_id='get_tweets',
        python_callable=get_tweets__,
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