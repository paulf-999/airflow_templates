#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : read_ip_from_dag_conf.py
* Description   : Read input from the DAG conf
* Created       : 28-09-2022
"""

__author__ = "Paul Fry"
__version__ = "0.1"

# Import default libraries, setup logging, create common variables
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, get_current_context
import logging

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# Setup paths, import libraries and templates (seldom needs to change)
dagpath, dagname, dagroot, helpers, queries, templates = setup_dag(__file__)  # noqa

# Create the DAG object and add/override the any parameters. To add/override any params, just list these after the `__file__` variable. See the example below:
# dag = get_dag_object(__file__, default_args={"email": "jbloggs@wesfarmers.com.au"}, tags=[""], aac_schedule_interval="30 8 * * *") # noqa
dag = get_dag_object(__file__, tags=["wip", "10"])  # noqa


def get_ips():

    context = get_current_context()
    # payload was the input passed into this Airflow DAG
    payload = context["dag_run"].conf

    division = payload["division"]
    src_tbl = payload["src_tbl"]

    """
    for key, value in payload.items():
        ip_tbl_list_dict = json.loads(value.replace("'", '"'))
        for division, tbl_list in ip_tbl_list_dict.items():
            logger.info(f"division = {division}")
            logger.info(f"tbl_list = {tbl_list}")

    logger.info(f"payload = {payload}")
    """

    logger.info(f"payload = {payload}")
    logger.info(f"division = {division}")
    logger.info(f"src_tbl = {src_tbl}")

    return payload, division, src_tbl


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
