from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, year, month, count, avg

spark = SparkSession.builder \
    .appName("TransformChicagoCrimes") \
    .getOrCreate()

input_path = "data/raw/chicago_crimes_raw"
output_path = "data/clean/chicago_crimes_clean"
analytics_path = "data/clean/daily_crime_summary"

df = spark.read.parquet(input_path)

# Clean column names
new_columns = [
    c.lower().replace(" ", "_").replace("-", "_")
    for c in df.columns
]
df = df.toDF(*new_columns)

# Parse date safely
df = df.withColumn(
    "date_clean",
    expr("try_to_timestamp(date, 'MM/dd/yyyy hh:mm:ss a')")
)

df = df.drop("date").withColumnRenamed("date_clean", "date")

# Remove bad rows
df = df.dropna(subset=["id", "case_number", "primary_type", "date"])

# Remove duplicates
df = df.dropDuplicates(["id"])

# Add partition columns
df = df.withColumn("year", year(col("date")))
df = df.withColumn("month", month(col("date")))

# Write clean detailed table
df.write.mode("overwrite") \
    .partitionBy("year", "month") \
    .parquet(output_path)

# Create daily analytics summary
daily_summary = df.groupBy("year", "month", "primary_type") \
    .agg(count("*").alias("crime_count"))

daily_summary.write.mode("overwrite") \
    .parquet(analytics_path)

print("Transform complete")
print(f"Clean output saved to: {output_path}")
print(f"Analytics summary saved to: {analytics_path}")

spark.stop()