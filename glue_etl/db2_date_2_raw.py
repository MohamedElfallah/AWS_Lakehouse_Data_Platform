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
    "url": "jdbc:mysql://15.237.13.14:3306/db2",
    "dbtable": "date",
    "user": "postgres",
    "password": "mytestdb",
    "customJdbcDriverS3Path": "s3://con-jdbc-drivers/mysql_driver.jar",
    "customJdbcDriverClassName": "com.mysql.cj.jdbc.Driver"}
df= glueContext.create_dynamic_frame.from_options(connection_type="postgresql", connection_options=connection_psql)
glueContext.write_dynamic_frame.from_options(
        frame = df,
        connection_type = "s3",    
        connection_options = {"path": "s3://mylake-raw-zone/db2/date/", "partitionKeys": []},
        format = "parquet")
job.commit()