from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from extract_data import get_URLs

max_pages = 5
def grab_URLS(max_pages):
    urls = get_URLs(max_pages)

    print(f"URLs to SEEK jobs found in the first {max_pages} pages.")
    for j, url enumerate urls:
        print(f"({j}): {url}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 3),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


# Define the DAG
dag = DAG(
    'grab_URLs',  # DAG name
    default_args=default_args,
    description='This DAG scrapes the URLs of data jobs in Sydney from SEEK.com'
)

# Define a task using PythonOperator
task = PythonOperator(
    task_id='grab_URLs',  # Task name
    python_callable=simple_task,  # Function to be called
    dag=dag,  # DAG to which this task belongs
)

# run task
task
