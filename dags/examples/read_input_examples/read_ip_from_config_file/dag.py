#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : read_ip_from_dag_conf.py
* Description   : Read input from the DAG conf
* Created       : 28-09-2022
"""

__author__ = "Paul Fry"
__version__ = "0.1"


import os
from includes import common
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
import logging
import json

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# Setup paths, import libraries and templates (seldom needs to change)
dag_name, dag_helpers, sql_queries, doc_md, logger, local_tz, default_args = common.get_common_dag_vars(__file__)  # noqa

dag_path = os.path.dirname(os.path.abspath(__file__))
dag_name = os.path.basename(dag_path)
dag_root = os.path.dirname(dag_path)


def get_ips():
    """Read input from config file. Returns shared input args used throughout the script."""

    with open(os.path.join(dag_path, "config.json")) as f:
        data = json.load(f)

    ip_list = data["example"]

    return ip_list


with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["example"]) as dag:

    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

    ####################################################################
    # DAG Lineage
    ####################################################################
    # for each source table read in, trigger the 'child' DAG
    for x in get_ips():
        example_task = BashOperator(task_id=f"task_{x}", bash_command=f"echo '{x}'")
        # Graph
        start_task >> example_task >> end_task
