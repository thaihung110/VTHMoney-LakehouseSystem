# Airflow DAGs

## Introduction

This directory contains Directed Acyclic Graphs (DAGs) for Apache Airflow. These DAGs define workflows for data processing and orchestration tasks.

## Directory Structure

- **import_marts_to_clickhouse.py**: A DAG for importing data marts into ClickHouse.
- **dbt_dremio_dag.py**: A DAG for orchestrating dbt tasks with Dremio.

## DAG Descriptions

### 1. import_marts_to_clickhouse.py

- **Purpose**: This DAG is designed to import data marts into ClickHouse.
- **Key Features**:
  - Defines tasks for extracting data from source systems.
  - Loads the extracted data into ClickHouse.
  - Handles dependencies between tasks to ensure proper execution order.
- **Usage**:
  - Trigger this DAG manually or set it to run on a schedule.
  - Monitor the execution through the Airflow UI.

### 2. dbt_dremio_dag.py

- **Purpose**: This DAG orchestrates dbt tasks to transform data in Dremio.
- **Key Features**:
  - Executes dbt commands to run models, tests, and generate documentation.
  - Integrates with Dremio for data transformations.
- **Usage**:
  - Trigger this DAG to run dbt transformations.
  - Ensure that the dbt profiles are correctly configured for Dremio.

## Running the DAGs

1. **Start Airflow**: Ensure that your Airflow instance is running. You can start it with:

   ```bash
        docker compose up airflow-webserver airflow-scheduler airflow-db -d
   ```

2. **Access the Airflow UI**: Open your browser and navigate to `http://localhost:8082`.

3. **Trigger DAGs**:
   - Find the DAGs in the Airflow UI.
   - Click on the DAG name to view details and trigger it manually or set a schedule.
