import os
from datetime import datetime

from airflow.operators.python import PythonOperator
from clickhouse_connect import get_client  # type: ignore
from minio import Minio  # type: ignore

from airflow import DAG

# MinIO config
MINIO_ENDPOINT = "minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password"
BUCKET_NAME = "warehouse"
MARTS_PREFIX = "marts/"

# ClickHouse config
CLICKHOUSE_HOST = "clickhouse"
CLICKHOUSE_USER = "admin"
CLICKHOUSE_PASSWORD = "password"

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 6, 1),
}

dag = DAG(
    "import_all_marts_from_minio",
    default_args=default_args,
    schedule_interval="0 1-23/3 * * *",  # Mỗi 3 tiếng bắt đầu từ 01:00
    catchup=False,
)


def list_parquet_files_from_minio():
    client = Minio(
        MINIO_ENDPOINT,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False,
    )

    parquet_files = []

    # Duyệt toàn bộ object bắt đầu từ 'marts/'
    objects = client.list_objects(
        BUCKET_NAME, prefix=MARTS_PREFIX, recursive=True
    )
    for obj in objects:
        if obj.object_name.endswith(".parquet"):
            parquet_files.append(obj.object_name)

    return parquet_files


def import_parquet_to_clickhouse():
    parquet_files = list_parquet_files_from_minio()

    ch_client = get_client(
        host=CLICKHOUSE_HOST,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
    )

    for path in parquet_files:
        # path: 'marts/dim_user/UUID/0_0_0.parquet'
        parts = path.split("/")
        if len(parts) < 3:
            continue  # Không hợp lệ
        table_name = parts[1]  # dim_user, dim_wallet, v.v.

        sql = f"""
        INSERT INTO marts.{table_name}
        SELECT * FROM s3(
            'http://minio:9000/warehouse/{path}',
            '{MINIO_ACCESS_KEY}', '{MINIO_SECRET_KEY}', 'Parquet'
        )
        """
        print(f"Importing into table: {table_name} from {path}")
        ch_client.command(sql)


# Task chính
import_task = PythonOperator(
    task_id="import_all_parquet",
    python_callable=import_parquet_to_clickhouse,
    dag=dag,
)
