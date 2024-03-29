#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : dbt_dag.py
* Description   : Boilerplate Airflow DAG script.
* Created       : 19-07-2021
* Usage         : python3 dbt_dag.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import logging
from airflow import DAG
from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtTestOperator
import pendulum

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

local_tz = pendulum.timezone("Australia/Melbourne")

# fmt: off
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "start_date": pendulum.now(local_tz).subtract(days=1)
}
# fmt: on

# fmt: off
with DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        default_args=default_args,
        schedule_interval=None,
        tags=["template"]
) as dag:

    # fmt: on

    # fmt: off
    # Failing tests would fail the task, and we don't want Airflow to try again
    dbt_test = DbtTestOperator(
        task_id="dbt_test",
        profiles_dir="profiles",
        models="curated_db",
        retries=0
    )
    # fmt: on

    dbt_run = DbtRunOperator(task_id="dbt_run", profiles_dir="profiles", models="analytics_db")

dbt_test >> dbt_run
