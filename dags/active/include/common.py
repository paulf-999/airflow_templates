#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : common.py
* Description   : Common DAG settings used
* Created       : 11-06-2022
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
logger.propagate = True

local_tz = pendulum.timezone("Australia/Melbourne")
default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": pendulum.now(local_tz).subtract(days=1)}


def get_common_dag_vars(ip_calling_dag):

    # Setup and import the filepaths used
    dag_path = os.path.dirname(os.path.abspath(ip_calling_dag))  # filepath of the DAG
    dag_name = os.path.basename(dag_path)  # name of the DAG (without the filepath)
    dag_root = os.path.dirname(dag_path)  # path of all dags

    if dag_root not in sys.path:
        sys.path.append(dag_root)

    # Import the DAG helper & SQL modules
    helpers = importlib.import_module(".__dag_helpers", package=dag_name)
    queries = importlib.import_module(".__sql_queries", package=dag_name)

    return dag_name, helpers, queries
