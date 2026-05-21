from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
from pathlib import Path

spark = SparkSession.builder \
    .appName("RawIngestChicagoCrimes") \
    .getOrCreate()

input_path = "data/chicago_crimes.csv"
output_path = "data/raw/chicago_crimes_raw"

if not Path(input_path).exists():
    raise FileNotFoundError(f"Input file not found: {input_path}")

df = spark.read.csv(
    input_path,
    header=True,
    inferSchema=False
)

print("Rows read:", df.count())

df = df.withColumn("ingestion_timestamp", current_timestamp()) \
       .withColumn("source_file", lit(input_path))

df.write.mode("overwrite").parquet(output_path)

print("Raw ingestion complete")
print(f"Output saved to: {output_path}")

spark.stop()
