import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)
connection_psql = {
    "url": "jdbc:postgresql://13.36.213.205:5432/db1",
    "dbtable": "event",
    "user": "postgres",
    "password": "mytestdb",
    "customJdbcDriverS3Path": "s3://con-jdbc-drivers/postgresql-42.4.2.jar",
    "customJdbcDriverClassName": "org.postgresql.Driver"}
df= glueContext.create_dynamic_frame.from_options(connection_type="postgresql", connection_options=connection_psql)
glueContext.write_dynamic_frame.from_options(
        frame = df,
        connection_type = "s3",    
        connection_options = {"path": "s3://mylake-raw-zone/db1/event/", "partitionKeys": []},
        format = "parquet")
job.commit()