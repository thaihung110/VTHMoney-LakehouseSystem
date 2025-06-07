-- Đặt thời gian checkpoint (tùy chọn)
SET 'execution.checkpointing.interval' = '10s';

-- Thiết lập các connector cần thiết
ADD JAR '/opt/flink/lib/flink-sql-connector-kafka.jar';
ADD JAR '/opt/flink/lib/flink-sql-connector-filesystem.jar';
ADD JAR '/opt/flink/lib/flink-parquet.jar';
ADD JAR '/opt/flink/lib/flink-sql-avro-confluent-registry.jar';