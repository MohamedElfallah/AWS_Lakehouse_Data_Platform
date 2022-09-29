import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import col
## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Extract 

df = glueContext.create_dynamic_frame.from_options(
    connection_type = "s3",
    connection_options = {"path":"s3://mylake-raw-zone/db2/date/"}, 
    format = "parquet" ).toDF()

# Transform 

df = df.withColumn("dateid", col("dateid").cast(IntegerType()))
df = df.withColumn("week", col("week").cast(IntegerType()))
df = df.withColumn("qtr", col("qtr").cast(IntegerType()))
df = df.withColumn("year", col("year").cast(IntegerType()))



# Load

glueContext.write_dynamic_frame.from_options(
    frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame"),
    connection_type = "s3",
    connection_options = {"path": "s3://mylake-processed-zone/db2/date/"},
    format = "parquet"
)

job.commit()