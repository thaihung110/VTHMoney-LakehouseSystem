FROM apache/airflow:2.10.5
WORKDIR /opt/airflow
USER root
RUN apt-get update && apt-get install -y git
COPY requirements.txt /opt/airflow/requirements.txt
USER airflow
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /opt/airflow/requirements.txt