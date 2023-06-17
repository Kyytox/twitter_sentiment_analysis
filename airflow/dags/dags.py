# # Airflow
# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.utils.dates import days_ago

# # librairies
# from datetime import datetime, timedelta
# import sys
# from pathlib import Path

# # Utils
# sys.path.append(str(Path(__file__).parent.parent.parent))
# # from aws.aws_utils import check_file_aws
# # from src.extraction_bronze import get_tweets


# # init Airflow DAG arguments
# default_args = {
#     'owner': 'admin',
#     # 'depends_on_past': False,
#     'retries': 3,
#     'retry_delay': timedelta(minutes=1),
# }


# # define the DAG
# dag = DAG(
#     dag_id='tweets_sentiment_analysis',
#     start_date=datetime(2023, 6, 16),
#     description='Get tweets for analysis sentiment with ML',
#     schedule_interval=timedelta(minutes=1),
# )  
    

# start = BashOperator(
#     task_id="start", 
#     bash_command="echo 42",
#     dag=dag)


# # # Task 1: check if file exists
# # # if not create it with infos of history_tech.xlsx
# # check_file_aws = PythonOperator(
# #     task_id='check_file_history_aws',
# #     python_callable=check_file_aws,
# #     op_kwargs={'key_file': "history_tech.parquet"},
# #     dag=dag
# # )

# # # Task 2: get tweets
# # get_tweets = PythonOperator(
# #     task_id='get_tweets',
# #     python_callable=get_tweets,
# #     dag=dag
# # )


# # Run tasks
# # start >> check_file_aws >> get_tweets
# start




from datetime import datetime, timedelta
from textwrap import dedent
import sys
from pathlib import Path

# Utils
sys.path.append(str(Path(__file__).parent.parent))
from plugins.operators.extraction_bronze import get_tweets
from plugins.operators.history_utils import create_history_tech

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


with DAG(
    "tweets_sentiment_analysis",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=10),
    },
    description="Get tweets for analysis sentiment with ML",
    schedule=timedelta(minutes=2),
    start_date=datetime(2023, 6, 16),
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
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
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
        python_callable=get_tweets,
        dag=dag
    )

    start >> check_history_tech >> get_tweets