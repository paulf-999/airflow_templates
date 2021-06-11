#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : template_dag.py
* Description   : Boilerplate Airflow DAG script.
* Created       : 11-06-2021
* Usage         : python3 template_dag.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import logging
from time import time
from airflow import DAG
from airflow import AirflowException
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

slack_token = Variable.get("slack_token")

def gen_op(**kwargs):
    """ generate sample op """
    START_TIME = time()
    logger.debug(f"Function called: get_user_ips()")

    ti = kwargs['ti']
    eg_op = []

    for i in range(0,4):
        eg_op.append(i)

    logger.info(f"eg_op = {eg_op}")

    logger.debug(f"Function finished: gen_op() finished in {round(time() - START_TIME, 2)} seconds")

    return eg_op

def read_op(**kwargs):
    """ read in sample op from subsequent step """
    START_TIME = time()
    logger.debug(f"Function called: get_user_ips()")

    ti = kwargs['ti']
    ip = ti.xcom_pull(task_ids='gen_op_eg')

    logger.info(f"ip = {ip}")

    for i in ip:
        logger.info(f"i = {i}")
        if i == 1:
            raise AirflowException(f"Example task error. i = 1")

    logger.debug(f"Function finished: read_op() finished in {round(time() - START_TIME, 2)} seconds")

    return

# SLACK_CHANNEL: the name of a slack channel to post task failure message
# SLACK_API_TOKEN
def slack_failure_msg(context):
    dag_id = context.get('task_instance').dag_id,
    task_id = context.get('task_instance').task_id,
    exec_date = context.get('execution_date').strftime('%Y-%m-%d/%H:%M'),
    log_url=context.get('task_instance').log_url
    
    failure_alert = SlackWebhookOperator(
        task_id='slack_failure_msg',
        http_conn_id='slack_connection',
        webhook_token=f'{slack_token}',
        channel='#airflow-integration',
        message=f'''Airflow Task Failed:\nAirflow DAG name: {dag_id}\nTask ID: {task_id}\nExec date: {exec_date}\nLog: {log_url}'''
    )
      
    failure_alert.execute(context=context)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': days_ago(1),
    'on_failure_callback': slack_failure_msg
}

with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        default_args=default_args,
        schedule_interval=None,
        tags=['wip','template', 'python']
    ) as dag:

    gen_op_tsk = PythonOperator(
        task_id="gen_op_eg", python_callable=gen_op, provide_context=True
    )

    read_op_tsk = PythonOperator(
        task_id="read_op_in_sub_task", python_callable=read_op, provide_context=True
    )

gen_op_tsk >> read_op_tsk
