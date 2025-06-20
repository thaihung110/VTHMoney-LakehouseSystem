from datetime import datetime

from airflow.operators.bash import BashOperator

from airflow import DAG

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    "dbt_dremio_run",
    default_args=default_args,
    schedule_interval="0 */3 * * *",  # Chạy mỗi 3 tiếng (vào phút 0 của giờ 0, 3, 6, 9, 12, 15, 18, 21)
    catchup=False,
) as dag:

    dbt_run_intermediate = BashOperator(
        task_id="dbt_run_intermediate",
        bash_command="cd /opt/airflow/dbt && dbt run --target intermediate --select models/intermediate",
    )

    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command="cd /opt/airflow/dbt && dbt run --target marts --select models/marts",
    )

    dbt_run_intermediate >> dbt_run_marts
