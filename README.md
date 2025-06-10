# Project Setup with Docker Compose

## Introduction

This project uses Docker Compose to manage multiple services, including PostgreSQL, Kafka, Debezium, Airflow, and more. This README provides instructions on how to set up and run the project using Docker.

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Services Overview

The following services are defined in the `docker-compose.yml`:

- **PostgreSQL**: Database service for storing application data.
- **Flinkr**: Service for managing streaming data.
- **Kafka**: Message broker for handling data streams.
- **Debezium**: Change data capture service for PostgreSQL.
- **Airflow**: Workflow orchestration service.
- **ClickHouse**: Analytical database.
- **Dremio**: Query engine on datalake
- **MinIO**: Object storage service.
- **Superset**: Data visualization tool.

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Build and Start Services

Run the following command to build and start all services defined in the `docker-compose.yml`:

```bash
docker-compose up -d
```

This command will:

- Pull the necessary Docker images.
- Create and start the containers in detached mode.
