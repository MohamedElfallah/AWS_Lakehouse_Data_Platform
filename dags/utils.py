import time 
import os
import boto3


def start_glue_job(job_name) :

        session = boto3.Session( aws_access_key_id= os.environ.get("AWS_ACESS_KEY"),
                                 aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                                 region_name="eu-west-3")
        glue_client = session.client("glue")
        job = glue_client.start_job_run(JobName= job_name)
        while True : 
            status = glue_client.get_job_run(JobName = job_name,RunId = job["JobRunId"])
            if status["JobRun"]["JobRunState"] == "SUCCEEDED" :
                break
            elif status["JobRun"]["JobRunState"] in ["FAILED", "ERROR", "TIMEOUT","STOPPED"]: 
                raise Exception("Something wrong happened during the job run")
            time.sleep(1)


def start_crawler(crawler_name) : 

    session = boto3.Session( aws_access_key_id= os.environ.get("AWS_ACESS_KEY"),
                                 aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
                                 region_name="eu-west-3")
    glue_client = session.client("glue")
    glue_client.start_crawler(Name = crawler_name)