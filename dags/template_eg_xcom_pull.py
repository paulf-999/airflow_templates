import os
import sys
import logging
from time import time
from datetime import datetime
from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': days_ago(1)
}

def gen_op(**kwargs):
    """ generate sample op """
    START_TIME = time()
    logger.debug(f"Function called: get_user_ips()")
    ti = kwargs['ti']
    eg_op = []

    for i in range(0,4):
        eg_op.append(i)

    return eg_op

def read_op(**kwargs):
    """ read in sample op from subsequent step """
    ti = kwargs['ti']
    ls = ti.xcom_pull(task_ids='gen_op_eg')

    return ls

with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        default_args=default_args,
        schedule_interval=None,
        tags=['python','template']
) as dag:
    gen_op_tsk = PythonOperator(
        task_id='gen_op_eg',
        python_callable=gen_op,
        provide_context=True
    )

    read_op_in_sub_tsk = PythonOperator(
        task_id="read_op_in_sub_task", python_callable=read_op, provide_context=True
    )

gen_op_tsk >> read_op_in_sub_tsk
