"""Example DAG demonstrating the usage of the BashOperator."""
from datetime import datetime

from airflow import DAG
from airflow.models.param import Param
from airflow.operators.bash import BashOperator
from airflow.operators.python import ShortCircuitOperator

with DAG(
    dag_id="example_bash_operator",
    params={
        "bucket_name": Param(default="s3_bucket_name", type="string"),
        "bucket_name": Param(default="s3_bucket_name", type="string"),
        "check_dbt": Param(default=False, type="boolean"),
    },
    schedule_interval=None,
    start_date=datetime.today(),
    tags=['example'],
    render_template_as_native_obj=True,
) as dag:
    run_this_last = BashOperator(
        task_id="run_this_last",
        bash_command="echo this is airflow s3 bucket: {{ dag_run.conf['bucket_name'] }}",
    )

    run_this = BashOperator(
        task_id="run_after_loop",
        bash_command='echo "after loop message"',
    )

    run_this >> run_this_last

    for i in range(3):
        task = BashOperator(
            task_id="runme_" + str(i),
            bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        )
        task >> run_this

    also_run_this = BashOperator(
        task_id="also_run_this",
        bash_command='echo "ti_key={{ task_instance_key_str }}"',
    )

    should_check_dbt = ShortCircuitOperator(
        task_id="check_dbt_precondition",
        python_callable=lambda x: x,
        op_args=["{{ params.check_dbt }}"]
    )

    check_dbt_installed = BashOperator(
        task_id="check_dbt_installed",
        bash_command='dbt --help',
    )

    also_run_this >> run_this_last >> should_check_dbt >> check_dbt_installed
