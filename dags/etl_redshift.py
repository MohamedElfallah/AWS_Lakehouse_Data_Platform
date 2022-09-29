from datetime import datetime
from airflow import DAG 
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator


sources ={
    "db1" : ["category", "event","venue"],
    "db2": ["sales", "listing", "date"],
    "db3" : ["users"]
}

default_args = {
    "owner" : "elfallah" , 
    "retries" : 0,
}

with DAG (
    dag_id = "load_to_redshift", 
    description= "Extract and Load data to redshift",
    schedule_interval= None, 
    start_date=datetime(2022,8,29),
    default_args= default_args
) as dag : 
    task1 = RedshiftSQLOperator(
        redshift_conn_id="con_redshift",
        task_id = "create_tables",
        sql = 'sql_scripts/create_tables.sql'         
    )
    tasks = []
    for source in sources.keys() :
        for table in sources[source]:
            task = S3ToRedshiftOperator(
                task_id = f"S3ToRedshift_{table}", 
                schema = "integrated",
                table = table,
                s3_bucket = "mylake-processed-zone",
                s3_key = f"{source}/{table}",
                aws_conn_id= "terraform_account", 
                redshift_conn_id= "con_redshift", 
                copy_options= ["FORMAT AS PARQUET"]
            )
            tasks.append(task)

    task1 >> tasks