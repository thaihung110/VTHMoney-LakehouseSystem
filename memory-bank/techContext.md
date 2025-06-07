# Technical Context

## System Components

### 1. Flink CDC Consumer

- Built with Apache Flink 1.17.1
- Uses jackson-datatype-jsr310 for timestamp handling
- Configured with log4j for logging
- Memory Configuration:
  ```
  Total Process Memory: 2048MB
  Framework Memory: 96MB (heap) + 96MB (off-heap)
  Task Memory: 512MB (heap) + 256MB (off-heap)
  Managed Memory: 512MB
  Network Memory: 64MB-128MB
  JVM Metaspace: 96MB
  JVM Overhead: 256MB-384MB
  ```

### 2. Data Generator

- Python-based data generation tool
- Uses psycopg2 for PostgreSQL connection
- Generates test data for:
  - Users
  - Wallets
  - Transactions
  - Notifications
  - Beneficiaries
- Basic timestamp handling through PostgreSQL's TIMESTAMP WITH TIME ZONE

### 3. PostgreSQL Database

- Version: 14
- CDC enabled with wal_level=logical
- Configured for replication
- Uses UUID for primary keys
- Timestamp fields use TIMESTAMP WITH TIME ZONE

### 4. Kafka & Zookeeper

- Kafka version: 7.3.0
- Zookeeper version: 7.3.0
- Used for CDC event streaming

### 5. Debezium

- Version: 2.3
- Configured for PostgreSQL CDC
- JSON message format

## Development Environment

- Java 11
- Maven for dependency management
- Docker and Docker Compose for containerization
- Windows development environment with WSL2 support

## Key Technical Decisions

1. Timestamp Handling:

   - Using UTC timezone for consistency
   - Java 8 date/time API with jackson-datatype-jsr310
   - PostgreSQL TIMESTAMP WITH TIME ZONE for database storage

2. Logging Strategy:

   - log4j for Java applications
   - Console and file appenders
   - Configurable log levels
   - Log rotation enabled

3. Memory Management:
   - Explicit memory configuration for Flink components
   - Balanced memory allocation for different operations
   - Configured JVM Overhead to prevent memory issues

## Technology Stack

### Data Processing & Streaming

- Apache Flink: Stream processing framework
- Apache Kafka: Message broker for real-time data streaming
- Debezium: Change Data Capture (CDC) platform

### Data Storage

- PostgreSQL: Source database system
- Data Warehouse (TBD)

### Infrastructure

- Docker: Containerization
- Docker Compose: Container orchestration

## Project Structure

```
.
├── Flink_Consumer/         # Flink streaming application
│   ├── src/               # Source code
│   ├── Dockerfile         # Flink container configuration
│   ├── pom.xml           # Maven dependencies
│   └── start-job.sh      # Job startup script
├── debezium/              # Debezium CDC configuration
│   ├── kraft/            # Kafka configuration
│   └── register-postgres.json  # Postgres connector config
├── database/              # Database related files
├── data_generator/        # Data generation utilities
└── docker-compose.yml     # Service orchestration
```

## Development Setup

1. Docker environment for containerized services
2. Apache Flink for stream processing
3. Kafka & Debezium for change data capture
4. PostgreSQL for source data

## Technical Constraints

1. Real-time data synchronization requirements
2. Data consistency across systems
3. Scalable architecture for growing data volumes
4. API performance for virtual assistant queries
