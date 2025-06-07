import os

import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# --- Config ---
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD", "password")
MINIO_BUCKET = "warehouse"
ICEBERG_WAREHOUSE = f"s3a://{MINIO_BUCKET}"
ICEBERG_DB = "staging.db"


# --- Helper: Load data from CSV ---
def load_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df


# --- Helper: Save DataFrame to Parquet ---
def save_parquet(df, path):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)


# --- Helper: Upload file to MinIO ---
def upload_to_minio(local_path, s3_path):
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )
    bucket, key = s3_path.replace("s3a://", "").split("/", 1)
    s3.upload_file(local_path, bucket, key)


# --- Main logic ---
def main():
    # Đọc dữ liệu từ file CSV
    transaction_types_df = load_data_from_csv("transaction_types.csv")
    payments_method_df = load_data_from_csv("payments_method.csv")

    # Lưu dữ liệu từ transaction_types vào Parquet
    local_parquet_transaction_types = "d:/VDT_Project/transaction_types.parquet"
    save_parquet(transaction_types_df, local_parquet_transaction_types)
    s3_parquet_transaction_types = f"s3a://{MINIO_BUCKET}/{ICEBERG_DB}/transaction_types/data/00000-0-0.parquet"
    upload_to_minio(
        local_parquet_transaction_types, s3_parquet_transaction_types
    )
    print(
        f"Uploaded Parquet for transaction_types to {s3_parquet_transaction_types}"
    )

    # Lưu dữ liệu từ payments_method vào Parquet
    local_parquet_payments_method = "d:/VDT_Project/payments_method.parquet"
    save_parquet(payments_method_df, local_parquet_payments_method)
    s3_parquet_payments_method = f"s3a://{MINIO_BUCKET}/{ICEBERG_DB}/payments_method/data/00000-0-0.parquet"
    upload_to_minio(local_parquet_payments_method, s3_parquet_payments_method)
    print(
        f"Uploaded Parquet for payments_method to {s3_parquet_payments_method}"
    )

    # --- Iceberg metadata creation ---
    print(
        "[INFO] Bạn cần dùng Spark hoặc Flink để hoàn tất commit snapshot Iceberg nếu PyIceberg chưa hỗ trợ ghi trực tiếp."
    )


if __name__ == "__main__":
    main()
