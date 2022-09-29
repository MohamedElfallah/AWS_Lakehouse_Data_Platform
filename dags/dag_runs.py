from datetime import datetime
from email.policy import default
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

raw_dags = ["db1_to_raw_zone","db2_to_raw_zone", "db3_to_raw_zone"]
processed_dags = ["db1_to_processed_zone", "db2_to_processed_zone", "db3_to_processed_zone"]


default_args = {
    "owner" :"elfallah",
    "retries" : "0",
}

with DAG(
    dag_id= "trigger_runs",
    description = "Dags trigger",
    schedule_interval= None,
    start_date= datetime(2022,8,31),
    default_args= default_args
) as dag :
    upstream = []
    for rdag in raw_dags : 
        task = TriggerDagRunOperator(
            task_id = f"trigger_{rdag}",
            trigger_dag_id= rdag,
            wait_for_completion= True,
            allowed_states= ["success"],
            poke_interval = 5
        )
        upstream.append(task)
    downstream = []
    for pdag in processed_dags :
        task = TriggerDagRunOperator(
            task_id=f"trigger_{pdag}",
            trigger_dag_id= pdag,
            wait_for_completion= True,
            allowed_states= ["success"],
            poke_interval=5
        )
        downstream.append(task)
    last_dag = TriggerDagRunOperator(
        task_id = "trigger_load_redshift",
        trigger_dag_id= "load_to_redshift",
        wait_for_completion=True,
        allowed_states=["success"],
        poke_interval = 5
    )
    upstream[0] >> downstream[0] 
    upstream[1] >> downstream[1] 
    upstream[2] >> downstream[2] 
    downstream >> last_dag
