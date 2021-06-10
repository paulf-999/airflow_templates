import os
import sys
import logging
from time import time
import boto3
from datetime import datetime
from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

AWS_ACCESS_KEY = Variable.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = Variable.get("AWS_SECRET_ACCESS_KEY")

dms_client = boto3.client('dms',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': days_ago(1)
}

def dms_check_task_status(**kwargs):
    """ Function to check the status of a DMS task """
    dms_task_name = kwargs['dag_run'].conf.get('dms_task_name')

    try:
        task = dms_client.describe_replication_tasks(
            Filters=[{'Name': 'replication-task-id','Values': [dms_task_name]}]
        )['ReplicationTasks'][0]

        logger.info(f"DMS task name: '{task['ReplicationTaskIdentifier']}'. Status: {task['Status']}")

        if task['Status'] == 'stopped':
            logger.info(f"DMS task name: {task['ReplicationTaskIdentifier']}. Status: {task['Status']}.\nReason: {task['StopReason']}")
        
        return task['Status']

    except:
        logger.info(f"ERROR checking the status of the task: {dms_task_name}. Please check.")

def start_task(**kwargs):
    """ Function to conditionally start a DMS task """
    dms_task_name = 'example-task'
    dms_task_status = 'ready'
    task = ''
    task_stop_status = ['stopped','failed','ready']
    ti = kwargs['ti']
    
    try:                  
        dms_task_arn = dms_client.describe_replication_tasks(
                    Filters=[{'Name': 'replication-task-id','Values': [dms_task_name]}]
        )['ReplicationTasks'][0]["ReplicationTaskArn"]

        logger.info(f"dms_task_arn = {dms_task_arn}")

        if dms_task_status in task_stop_status:
            logger.info('DMS Task in stopped status. Proceeding to start the DMS replication.')

            try:
                task = dms_client.start_replication_task(
                    ReplicationTaskArn=dms_task_arn,
                    StartReplicationTaskType='start-replication'
                )['ReplicationTask']
                
            except Exception as e:
                logger.info("Starting DMS Task with StartReplicationTaskType as 'reload-target'")
                if 'START_REPLICATION, valid only for tasks running for the first time' in str(e):
                    task = dms_client.start_replication_task(
                        ReplicationTaskArn=dms_task_arn,
                        StartReplicationTaskType='reload-target',
                    )['ReplicationTask']
                else:
                    logger.error(e)

            logger.info(f"DMS task '{task['ReplicationTaskIdentifier']}' has started successfully")

            return task['Status']

    except:
        logger.info(f"ERROR starting the DMS task - {task['ReplicationTaskIdentifier']}. Please check DMS task: {dms_task_name}")

with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        default_args=default_args,
        schedule_interval=None,
        tags=['python','template']
) as dag:
    describe_dms_tasks = PythonOperator(
        task_id='get_dms_task_status',
        python_callable=dms_check_task_status,
        provide_context=True
    )
