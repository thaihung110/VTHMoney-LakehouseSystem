-- ocker exec -it clickhouse clickhouse-client --host=clickhouse --port=9000 --user=admin --password=password


CREATE TABLE IF NOT EXISTS marts.dim_payment_method (
    id Int64,
    code Nullable(String),
    name Nullable(String),
    description Nullable(String)
) 
ENGINE = MergeTree()
ORDER BY id;


CREATE TABLE IF NOT EXISTS marts.dim_transaction_type (
    id Int64,
    code Nullable(String),
    name Nullable(String),
    description Nullable(String)
) 
ENGINE = MergeTree()
ORDER BY id;


CREATE TABLE IF NOT EXISTS marts.dim_date (
    date_day Date
) 
ENGINE = MergeTree()
ORDER BY date_day;


CREATE TABLE IF NOT EXISTS marts.dim_user (
    id String,
    full_name Nullable(String),
    email Nullable(String),
    phone_number Nullable(String),
    gender Nullable(String),
    status Nullable(String),
    created_at Nullable(DateTime)
) 
ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS marts.dim_wallet (
    id String,
    user_id Nullable(String),
    currency Nullable(String),
    status Nullable(String),
    created_at Nullable(DateTime)
) 
ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS marts.fact_transactions (
    id String,
    transaction_type_id Nullable(Int32),
    payment_method_id Nullable(Int32),
    sender_wallet_id Nullable(String),
    sender_user_id Nullable(String),
    receiver_wallet_id Nullable(String),
    receiver_user_id Nullable(String),
    amount Nullable(Decimal(20, 4)),
    currency Nullable(String),
    fee_amount Nullable(Decimal(20, 4)),
    status Nullable(String),
    description Nullable(String),
    reference_number Nullable(String),
    created_at Nullable(DateTime),
    updated_at Nullable(DateTime),
    transaction_date Nullable(Date)
) 
ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE IF NOT EXISTS marts.transaction_daily_summary (
    transaction_date Date,
    transaction_type_id Int32,
    transaction_type_name Nullable(String),
    payment_method_id Int32,
    payment_method_name Nullable(String),
    status Nullable(String),
    total_transactions Nullable(Int64),
    total_amount Nullable(Decimal(38, 4)),
    total_fee Nullable(Decimal(38, 4))
) 
ENGINE = MergeTree()
ORDER BY (transaction_date, transaction_type_id, payment_method_id);

CREATE TABLE IF NOT EXISTS marts.user_transaction_summary (
    user_id String,
    full_name Nullable(String),
    status Nullable(String),
    total_transactions Nullable(Int64),
    total_amount Nullable(Decimal(38, 4))
) 
ENGINE = MergeTree()
ORDER BY user_id;
