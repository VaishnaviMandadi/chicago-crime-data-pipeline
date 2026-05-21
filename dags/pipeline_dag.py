from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT_DIR = "/opt/airflow"

default_args = {
    "owner": "vaishnavi",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="chicago_crime_batch_pipeline",
    default_args=default_args,
    description="End-to-end batch pipeline for Chicago crime data",
    start_date=datetime(2026, 5, 20),
    schedule="@daily",
    catchup=False,
) as dag:

    raw_ingest = BashOperator(
        task_id="raw_ingest",
        bash_command=f"cd {PROJECT_DIR} && python jobs/raw_ingest.py",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=f"cd {PROJECT_DIR} && python jobs/transform.py",
    )

    quality_checks = BashOperator(
        task_id="quality_checks",
        bash_command=f"cd {PROJECT_DIR} && python jobs/gx_quality_checks.py",
    )

    raw_ingest >> transform >> quality_checks