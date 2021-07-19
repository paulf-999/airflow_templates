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
from airflow.utils.dates import days_ago

from airflow.operators.python_operator import PythonOperator

# from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": days_ago(1)}


def function_to_call():

    print("abc")

    return


with DAG(dag_id=os.path.basename(__file__).replace(".py", ""), default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    data_quality_rule_1 = PythonOperator(task_id="data_quality_rule_1", python_callable=function_to_call, provide_context=True)

    data_quality_rule_2 = PythonOperator(task_id="data_quality_rule_2", python_callable=function_to_call, provide_context=True)

    data_quality_rule_3 = PythonOperator(task_id="data_quality_rule_3", python_callable=function_to_call, provide_context=True)

    data_quality_rule_4 = PythonOperator(task_id="data_quality_rule_4", python_callable=function_to_call, provide_context=True)

    data_quality_rule_5 = PythonOperator(task_id="data_quality_rule_5", python_callable=function_to_call, provide_context=True)

    data_quality_rule_6 = PythonOperator(task_id="data_quality_rule_6", python_callable=function_to_call, provide_context=True)

    data_quality_rule_7 = PythonOperator(task_id="data_quality_rule_7", python_callable=function_to_call, provide_context=True)

    data_quality_rule_1_1 = PythonOperator(task_id="data_quality_rule_1.1", python_callable=function_to_call, provide_context=True)

    data_quality_rule_2_1 = PythonOperator(task_id="data_quality_rule_2.1", python_callable=function_to_call, provide_context=True)

    data_quality_rule_3_1 = PythonOperator(task_id="data_quality_rule_3.1", python_callable=function_to_call, provide_context=True)

data_quality_rule_1_1.set_upstream(data_quality_rule_1)

data_quality_rule_2_1.set_upstream(data_quality_rule_2)

data_quality_rule_3_1.set_upstream(data_quality_rule_3)