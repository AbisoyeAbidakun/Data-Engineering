from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

from airflow.utils.dates import days_ago

from run_ETL_spotify import run_load_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='ETL process!',
    schedule_interval=timedelta(days=1),
)


def just_a_function():
    print("I'm going to show you something :)")


run_etl = PythonOperator(
    task_id='whole_spotify_etl',
    python_callable=run_load_etl,
    dag=dag,
)

send_email = EmailOperator(task_id='send_email',
                           to='tony.xu@airflow.com',
                           subject='Daily report on spotify tracks',
                           dag=dag)

run_etl >> send_email
