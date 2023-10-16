#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : template_dag_standalone.py
* Description   : Boilerplate Airflow DAG. Doesn't use a shared/common package lib.
* Created       : 11-06-2021
"""

__author__ = "Paul Fry"
__version__ = "1.0"

import os
import sys
import logging
import importlib
import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

local_tz = pendulum.timezone("Europe/Dublin")
dag_path = os.path.dirname(os.path.abspath(__file__))
dag_name = os.path.basename(dag_path)
dag_root = os.path.dirname(dag_path)

if dag_root not in sys.path:
    sys.path.append(dag_root)

helpers = importlib.import_module(".__dag_helpers", package=dag_name)
queries = importlib.import_module(".__sql_queries", package=dag_name)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "start_date": pendulum.now(local_tz).subtract(days=1),
}

doc_md = helpers.try_render_readme(dag_path)

conn_id = "dm_snowflake_conn"

with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["10"]) as dag:
    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = EmptyOperator(task_id="start")
    end_task = EmptyOperator(task_id="end")

    sf_query_eg1 = SnowflakeOperator(task_id="sf_query_eg1", sql=queries.example_query, snowflake_conn_id=conn_id)

####################################################################
# DAG Lineage
####################################################################
start_task >> sf_query_eg1 >> end_task
