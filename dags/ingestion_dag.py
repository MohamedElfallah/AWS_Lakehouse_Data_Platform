from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import os

default_args = {
    "owner": "airflow",
    "retries":5,
    "retry_delay": timedelta(minutes= 1)
}

with DAG(
    dag_id= "ingest_data_airflow",
    schedule_interval= "@daily",
    start_date= datetime(2022,7,12),
    default_args=default_args,
) as ingestion_dag:
    
    def download_data():
        import os
        AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
        print("Downloaading........")
        URL_TEMPLATE = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet"
        os.system(f"curl {URL_TEMPLATE} > {AIRFLOW_HOME}/output.parquet")
        print("Done !!!")


    def push_to_pgdb(host, port, user, password, db, table):
        import sqlalchemy
        import pyarrow.dataset as ds
        import pandas as pd
        import os

        AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME")
        engine = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
        data = ds.dataset(f"{AIRFLOW_HOME}/output.parquet", format="parquet")
        schema = data.head(0).to_pandas()
        schema.to_sql(name = table, con = engine,if_exists = "replace")

        batches = data.to_batches(batch_size = 10000)
        for i in range(4):
            batch = next(iter(batches))
            b= batch.to_pandas()
            b.to_sql(name= table, con = engine, if_exists = "append")
            print("done with batch : ", i)



    task1 = PythonOperator(
        task_id = "download_data",
        python_callable=download_data
    )

    task2 = PythonOperator(
        task_id = "push_data_topgdb",
        python_callable= push_to_pgdb,
        op_kwargs= {
            "host": os.environ.get("PG_HOST"),
            "user": os.environ.get("PG_USER"),
            "password": os.environ.get("PG_PASSWORD"),
            "db": "taxi",
            "port": "5432",
            "table": "taxi_data"
        }
    )
    task1 >> task2


    
    