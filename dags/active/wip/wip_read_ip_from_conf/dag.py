#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : read_ip_from_dag_conf.py
* Description   : Read input from the DAG conf
* Created       : 28-09-2022
"""

__author__ = "Paul Fry"
__version__ = "0.1"


from includes import common
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, get_current_context
import logging

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# Setup paths, import libraries and templates (seldom needs to change)
dag_name, dag_helpers, sql_queries, doc_md, logger, local_tz, default_args = common.get_common_dag_vars(__file__)  # noqa


def get_ips():

    context = get_current_context()
    # payload was the input passed into this Airflow DAG
    payload = context["dag_run"].conf

    division = payload["division"]
    src_tbl = payload["src_tbl"]

    logger.info(f"payload = {payload}")
    logger.info(f"division = {division}")
    logger.info(f"src_tbl = {src_tbl}")

    return payload, division, src_tbl


with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    # Create tasks
    start_task = DummyOperator(task_id="start", dag=dag)
    end_task = DummyOperator(task_id="end", dag=dag)

    get_input = PythonOperator(task_id="get_input", python_callable=get_ips)

    # TODO (return to)
    # echo_task = BashOperator(task_id="echo_task", bash_command="echo 'example task!'", dag=dag)

    # Create graph
    start_task >> get_input >> end_task

    # done - part 1 - pass input
    # done - part 2 - read in input from a file
    # in progress - part 3 - loop through entries
