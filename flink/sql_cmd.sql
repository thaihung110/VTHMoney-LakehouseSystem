--docker exec -it flink ./bin/sql-client.sh

SET 'execution.runtime-mode' = 'streaming';
SET 'sql-client.execution.result-mode' = 'tableau';
SET 'execution.checkpointing.interval' = '30s';
SET 'parallelism.default' = '1';

-- tạo source table 
CREATE TABLE default_catalog.default_database.users_cdc (
    id STRING,
    phone_number STRING,
    email STRING,
    full_name STRING,
    date_of_birth INT,
    gender STRING,
    status STRING,
    password_hash STRING,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'connector' = 'kafka',
    'topic' = 'vth_money.public.users',
    'properties.bootstrap.servers' = 'kafka:9092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'properties.max.poll.records' = '100',
    'debezium-json.timestamp-format.standard' = 'ISO-8601'  -- tùy chọn, thường mặc định đã đúng
);

CREATE TABLE default_catalog.default_database.beneficiaries_cdc (
    id STRING,
    user_id STRING,
    beneficiary_name STRING,
    beneficiary_phone STRING,
    beneficiary_bank_code STRING,
    beneficiary_bank_account STRING,
    beneficiary_bank_branch STRING,
    is_favorite BOOLEAN,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'connector' = 'kafka',
    'topic' = 'vth_money.public.beneficiaries',
    'properties.bootstrap.servers' = 'kafka:9092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'properties.max.poll.records' = '100',
    'debezium-json.timestamp-format.standard' = 'ISO-8601'
);

CREATE TABLE default_catalog.default_database.transactions_cdc (
    id STRING,
    transaction_type_id INT,
    payment_method_id INT,
    sender_id STRING,
    receiver_id STRING,
    sender_wallet_id STRING,
    receiver_wallet_id STRING,
    amount DECIMAL(20, 4),
    currency STRING,
    fee_amount DECIMAL(20, 4),
    status STRING,
    description STRING,
    reference_number STRING,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'connector' = 'kafka',
    'topic' = 'vth_money.public.transactions',
    'properties.bootstrap.servers' = 'kafka:9092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'properties.max.poll.records' = '100',
    'debezium-json.timestamp-format.standard' = 'ISO-8601'
);


CREATE TABLE default_catalog.default_database.notifications_cdc (
    id STRING,
    user_id STRING,
    transaction_id STRING,
    title STRING,
    message STRING,
    is_read BOOLEAN,
    created_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'connector' = 'kafka',
    'topic' = 'vth_money.public.notifications',
    'properties.bootstrap.servers' = 'kafka:9092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'properties.max.poll.records' = '100',
    'debezium-json.timestamp-format.standard' = 'ISO-8601'
);

CREATE TABLE default_catalog.default_database.wallets_cdc (
    id STRING,
    user_id STRING,
    balance DECIMAL(20, 4),
    currency STRING,
    status STRING,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'connector' = 'kafka',
    'topic' = 'vth_money.public.wallets',
    'properties.bootstrap.servers' = 'kafka:9092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'debezium-json',
    'properties.max.poll.records' = '100',
    'debezium-json.timestamp-format.standard' = 'ISO-8601'
);


select * from default_catalog.default_database.users_cdc;

CREATE CATALOG c_iceberg_hive WITH (
    'type' = 'iceberg',
    'catalog-type'='hive',
    'warehouse' = 's3a://warehouse',
    'hive-conf-dir' = './conf');

USE CATALOG c_iceberg_hive;

CREATE DATABASE IF NOT EXISTS c_iceberg_hive.staging;
USE c_iceberg_hive.staging;


CREATE TABLE c_iceberg_hive.staging.users_iceberg (
    id STRING,
    phone_number STRING,
    email STRING,
    full_name STRING,
    date_of_birth INT,
    gender STRING,
    status STRING,
    password_hash STRING,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'write.target-file-size-bytes' = '16000000', -- 32MB nếu bị OOM
    'sink.commit-interval' = '2s'
);

CREATE TABLE c_iceberg_hive.staging.beneficiaries_iceberg (
    id STRING,
    user_id STRING,
    beneficiary_name STRING,
    beneficiary_phone STRING,
    beneficiary_bank_code STRING,
    beneficiary_bank_account STRING,
    beneficiary_bank_branch STRING,
    is_favorite BOOLEAN,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'write.target-file-size-bytes' = '16000000', -- 32MB nếu bị OOM
    'sink.commit-interval' = '2s'
);

CREATE TABLE c_iceberg_hive.staging.transactions_iceberg (
    id STRING,
    transaction_type_id INT,
    payment_method_id INT,
    sender_id STRING,
    receiver_id STRING,
    sender_wallet_id STRING,
    receiver_wallet_id STRING,
    amount DECIMAL(20, 4),
    currency STRING,
    fee_amount DECIMAL(20, 4),
    status STRING,
    description STRING,
    reference_number STRING,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'write.target-file-size-bytes' = '16000000', -- 32MB nếu bị OOM
    'sink.commit-interval' = '2s'
);

CREATE TABLE c_iceberg_hive.staging.notifications_iceberg (
    id STRING,
    user_id STRING,
    transaction_id STRING,
    title STRING,
    message STRING,
    is_read BOOLEAN,
    created_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'write.target-file-size-bytes' = '16000000', -- 32MB nếu bị OOM
    'sink.commit-interval' = '2s'
);


CREATE TABLE c_iceberg_hive.staging.wallets_iceberg (
    id STRING,
    user_id STRING,
    balance DECIMAL(20, 4),
    currency STRING,
    status STRING,
    created_at TIMESTAMP_LTZ(6),
    updated_at TIMESTAMP_LTZ(6),
    PRIMARY KEY (id) NOT ENFORCED
)
WITH (
    'write.target-file-size-bytes' = '16000000', -- 32MB nếu bị OOM
    'sink.commit-interval' = '2s'
);


USE CATALOG default_catalog;

-- Insert dữ liệu từ CDC source vào Iceberg sink
INSERT INTO c_iceberg_hive.staging.users_iceberg 
SELECT * FROM default_catalog.default_database.users_cdc;

INSERT INTO c_iceberg_hive.staging.beneficiaries_iceberg 
SELECT * FROM default_catalog.default_database.beneficiaries_cdc;

INSERT INTO c_iceberg_hive.staging.transactions_iceberg
SELECT * FROM default_catalog.default_database.transactions_cdc;

INSERT INTO c_iceberg_hive.staging.notifications_iceberg
SELECT * FROM default_catalog.default_database.notifications_cdc;

INSERT INTO c_iceberg_hive.staging.wallets_iceberg 
SELECT * FROM default_catalog.default_database.wallets_cdc;





