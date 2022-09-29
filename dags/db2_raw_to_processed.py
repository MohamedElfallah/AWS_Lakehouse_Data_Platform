from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.python import PythonOperator
from utils import start_crawler, start_glue_job

jobs_name = ["process_date.py", "process_listing.py", "process_sales.py"]


default_args = {
    "owner" : "elfallah", 
    "retries": "0",
    "retry_delay" : timedelta(seconds=30)
}

with DAG(
    dag_id= "db2_to_processed_zone",
    description= "Ingest Source Data to DataLake's Raw zone",
    schedule_interval= None,
    start_date= datetime(2022,8,28),
    default_args= default_args 
) as ingest_raw_dag : 
            
    ingestion_tasks = []
    for job in jobs_name : 
        task = PythonOperator(
            task_id=job,
            python_callable= start_glue_job,
            op_kwargs= {"job_name" : job}
        ) 
        ingestion_tasks.append(task) 
    
    crawler_task = PythonOperator(
        task_id = "start_crawler",
        python_callable = start_crawler,
        op_kwargs= {"crawler_name" : "processed-db2-crawler"} 
    )
    
    ingestion_tasks >> crawler_task



