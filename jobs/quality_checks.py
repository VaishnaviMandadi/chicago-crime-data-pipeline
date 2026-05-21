from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp

spark = SparkSession.builder \
    .appName("QualityChecksChicagoCrimes") \
    .getOrCreate()

input_path = "data/clean/chicago_crimes_clean"

df = spark.read.parquet(input_path)

total_rows = df.count()
null_id_rows = df.filter(col("id").isNull()).count()
null_case_rows = df.filter(col("case_number").isNull()).count()
null_type_rows = df.filter(col("primary_type").isNull()).count()
null_date_rows = df.filter(col("date").isNull()).count()
future_date_rows = df.filter(col("date") > current_timestamp()).count()

print("Total rows:", total_rows)
print("Null ID rows:", null_id_rows)
print("Null case_number rows:", null_case_rows)
print("Null primary_type rows:", null_type_rows)
print("Null date rows:", null_date_rows)
print("Future date rows:", future_date_rows)

if total_rows == 0:
    raise Exception("Data quality failed: clean table has zero rows")

if null_id_rows > 0:
    raise Exception("Data quality failed: null id values found")

if null_case_rows > 0:
    raise Exception("Data quality failed: null case_number values found")

if null_type_rows > 0:
    raise Exception("Data quality failed: null primary_type values found")

if null_date_rows > 0:
    raise Exception("Data quality failed: null date values found")

if future_date_rows > 0:
    raise Exception("Data quality failed: future dates found")

print("All data quality checks passed!")

spark.stop()