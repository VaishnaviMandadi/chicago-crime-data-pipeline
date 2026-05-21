# Chicago Crime Batch Pipeline

End-to-end batch data pipeline using Chicago crime data.

## Tech Stack

- Python
- PySpark
- Apache Airflow
- Docker
- Parquet
- Data quality checks

## Architecture

Chicago Crimes CSV
→ Raw Ingestion
→ Raw Parquet
→ Transformation
→ Clean Partitioned Parquet
→ Data Quality Checks
→ Analytics Tables

## Airflow DAG

DAG name:

`chicago_crime_batch_pipeline`

Task order:

`raw_ingest >> transform >> quality_checks`

## Output Tables

### Raw Zone

`data/raw/chicago_crimes_raw`

### Clean Zone

`data/clean/chicago_crimes_clean`

Partitioned by:

- year
- month

### Analytics Summary

`data/clean/daily_crime_summary`

## Data Quality Checks

The pipeline checks:

- table is not empty
- id is not null
- case_number is not null
- primary_type is not null
- date is not null
- no future dates

## Run with Docker

```bash
docker compose up --build