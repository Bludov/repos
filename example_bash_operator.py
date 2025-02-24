from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

from dags.etl.test import load_worker

default_args = {
    'owner': 'GB',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG(
    'example_bash_operator',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    max_active_runs=1
)

task_load_worker = PythonOperator(
    task_id='1st_dag_run_id',
    python_callable=load_worker,
    dag=dag,
    provide_context=True,
)

task_load_worker
