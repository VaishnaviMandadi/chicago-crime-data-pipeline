from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

spark = SparkSession.builder \
    .appName("GreatExpectationsStyleChecks") \
    .getOrCreate()

input_path = "data/clean/chicago_crimes_clean"

df = spark.read.parquet(input_path)

checks = {
    "table_has_rows": df.count() > 0,
    "id_has_no_nulls": df.filter(col("id").isNull()).count() == 0,
    "case_number_has_no_nulls": df.filter(col("case_number").isNull()).count() == 0,
    "primary_type_has_no_nulls": df.filter(col("primary_type").isNull()).count() == 0,
    "date_has_no_nulls": df.filter(col("date").isNull()).count() == 0,
    "no_future_dates": df.filter(col("date") > current_timestamp()).count() == 0,
}

failed_checks = [name for name, passed in checks.items() if not passed]

if failed_checks:
    raise Exception(f"Data quality failed: {failed_checks}")

print("Great Expectations-style checks passed!")

spark.stop()