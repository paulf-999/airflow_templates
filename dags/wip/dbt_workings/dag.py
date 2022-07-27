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
from airflow.operators.bash import BashOperator
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

dbt_project_dir = "<PATH TO DBT_PROJECT_FOLDER>"

doc_md = helpers.try_render_readme(dag_path)

with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:
    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")
    # py_op_eg = PythonOperator(task_id="py_op_eg", python_callable=write_op)

    # note: the jinja below needs to be escaped (i.e., double up every curly bracket), as an f-string is as used an input for the bash_command
    bash_operator_eg = BashOperator(task_id="dbt_conn_test", bash_command=f"set -e; cd {dbt_project_dir}; dbt {{{{ dag_run.conf['src_tbl'] }}}} --profiles-dir profiles", dag=dag, retries=0)

    # works
    """
    bash_operator_eg = BashOperator(
        task_id="dbt_conn_test", bash_command="set -e; dbt debug --project-dir /opt/airflow/dags/dbt/dbt_ofw --profiles-dir /opt/airflow/dags/dbt/dbt_ofw/profiles", dag=dag, retries=0
    )
    """

    # works w/ip
    """
    bash_operator_eg = BashOperator(
        task_id="dbt_conn_test", bash_command="set -e; cd /opt/airflow/dags/dbt/dbt_ofw; dbt {{ ti.xcom_pull(task_ids='py_op_eg') }} --profiles-dir profiles", dag=dag, retries=0
    )
    """

    # works w/ip & using an f-string (need to escape jinja)
    """
    bash_operator_eg = BashOperator(task_id="dbt_conn_test", bash_command=f"set -e; cd {dbt_project_dir}; dbt {{{{ ti.xcom_pull(task_ids='py_op_eg') }}}} --profiles-dir profiles", dag=dag, retries=0)
    """

    # works w/ip from xcom & f-string
    """
    bash_operator_eg = BashOperator(
        task_id="dbt_conn_test", bash_command=f"echo \"here. {beep}. is the message: '$src_tbl'\"", env={"src_tbl": '{{ dag_run.conf["src_tbl"] if dag_run else "" }}'}, dag=dag, retries=0
    )
    """

    # BASELINED!
    # bash_operator_eg = BashOperator(task_id="dbt_conn_test", bash_command=f"set -e; cd {dbt_project_dir}; dbt {{{{ dag_run.conf['src_tbl'] }}}} --profiles-dir profiles", dag=dag, retries=0)

    # Create graph
    # start_task >> py_op_eg >> bash_operator_eg >> end_task
    start_task >> bash_operator_eg >> end_task
