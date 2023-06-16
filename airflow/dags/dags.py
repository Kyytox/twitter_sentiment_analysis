# # Airflow
# from airflow import DAG
# from airflow.operators.python import PythonOperator
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

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
with DAG(
    "tutorial",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function, # or list of functions
        # 'on_success_callback': some_other_function, # or list of functions
        # 'on_retry_callback': another_function, # or list of functions
        # 'sla_miss_callback': yet_another_function, # or list of functions
        # 'trigger_rule': 'all_success'
    },
    description="A simple tutorial DAG",
    schedule=timedelta(minutes=3),
    start_date=datetime(2023, 6, 16),
    catchup=False,
    tags=["example"],
) as dag:

    # t1, t2 and t3 are examples of tasks created by instantiating operators
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date",
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3,
    )
    t1.doc_md = dedent(
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

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
    )

    t1 >> [t2, t3]