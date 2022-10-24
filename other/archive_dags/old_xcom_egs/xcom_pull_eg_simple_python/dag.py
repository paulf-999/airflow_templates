#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : template_dag.py
* Description   : Boilerplate Airflow DAG.
* Created       : 11-06-2021
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
import logging
import importlib
import pendulum
from time import time
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

local_tz = pendulum.timezone("Australia/Melbourne")
dag_path = os.path.dirname(os.path.abspath(__file__))
dag_name = os.path.basename(dag_path)
dag_root = os.path.dirname(dag_path)

if dag_root not in sys.path:
    sys.path.append(dag_root)

helpers = importlib.import_module(".__dag_helpers", package=dag_name)
queries = importlib.import_module(".__sql_queries", package=dag_name)

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": pendulum.now(local_tz).subtract(days=1)}

doc_md = helpers.try_render_readme(dag_path)


def gen_op(**kwargs):
    """generate sample op"""
    START_TIME = time()
    logger.debug("Function called: get_user_ips()")

    eg_op = []

    for i in range(0, 4):
        eg_op.append(i)

    logger.debug(f"Function finished: gen_op() finished in {round(time() - START_TIME, 2)} seconds")

    return eg_op


def read_op(**kwargs):
    """read in sample op from subsequent step"""
    START_TIME = time()
    logger.debug("Function called: get_user_ips()")

    ti = kwargs["ti"]
    xcom_pull = ti.xcom_pull(task_ids="gen_op_eg")

    logger.debug(f"Function finished: read_op() finished in {round(time() - START_TIME, 2)} seconds")

    return xcom_pull


with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

    gen_op_tsk = PythonOperator(task_id="gen_op_eg", python_callable=gen_op)

    read_op_in_sub_tsk = PythonOperator(task_id="read_op_in_sub_task", python_callable=read_op)

####################################################################
# DAG Lineage
####################################################################
start_task >> gen_op_tsk >> read_op_in_sub_tsk >> end_task
