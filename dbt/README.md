# DBT Project

## Introduction

This project utilizes dbt (data build tool) for transforming and modeling data. It allows users to define data transformations in SQL and manage them efficiently.

## Directory Structure

- **dremio_dbt/**: Contains dbt models and configurations.
- **profiles.yml**: Configuration file for dbt profiles.
- **.user.yml**: User-specific configurations.
- **logs/**: Directory for dbt logs.

## Requirements

Before running the dbt project, ensure you have the following installed:

- [dbt](https://docs.getdbt.com/docs/installation) (follow the installation instructions for your environment)
- A compatible data warehouse (e.g., Dremio, Snowflake, BigQuery, etc.)

## Configuration

1. **Profiles Configuration**:

   - Open the `profiles.yml` file and configure your connection settings for your data warehouse. Here’s an example configuration for Dremio:

   ```yaml
   dev:
   outputs:
     local:
       dremio_space: "@user"
       dremio_space_folder: no_schema
       object_storage_path: no_schema
       object_storage_source: lakehouse
       password: <your-password>
       port: 9047
       software_host: localhost
       threads: 1
       type: dremio
       use_ssl: false
       user: <your-username>
     dev:
       dremio_space: "@user"
       dremio_space_folder: no_schema
       object_storage_path: no_schema
       object_storage_source: lakehouse
       password: <your-password>
       port: 9047
       software_host: dremio
       threads: 1
       type: dremio
       use_ssl: false
       user: <your-username>
   target: local
   ```

2. **User Configuration**:
   - The `.user.yml` file can be used for user-specific settings. Ensure it contains the necessary configurations for your environment.

## Running the Project

1. **Navigate to the dbt directory**:

   ```bash
    cd dbt/dremio_dbt/
   ```

2. **Run dbt commands**:

   - To run your dbt models, use the following command:

   ```bash
   dbt run
   ```

   - To test your models, use:

   ```bash
   dbt test
   ```

   - To generate documentation, use:

   ```bash
   dbt docs generate
   dbt docs serve
   ```

## Logs

- Check the `logs/` directory for any logs generated during the dbt runs. This can help in debugging issues.

## Notes

- Ensure that your data warehouse is accessible and that you have the necessary permissions to run dbt commands.
