import importlib
import logging
import os
import sys

import pendulum
from airflow.models.dagbag import DagBag

local_tz = pendulum.timezone("Australia/Melbourne")


def get_common_dag_vars(ip_calling_dag):
    """retrieve commononly used/shared variables"""

    # Setup and import the filepaths used
    dag_path = os.path.dirname(os.path.abspath(ip_calling_dag))  # filepath of the DAG
    dag_name = os.path.basename(dag_path)  # name of the DAG (without the filepath)
    dag_root = os.path.dirname(dag_path)  # path of all dags

    if dag_root not in sys.path:
        sys.path.append(dag_root)

    # Import the DAG helper & SQL modules
    dag_helpers = importlib.import_module(".__dag_helpers", package=dag_name)
    sql_queries = importlib.import_module(".__sql_queries", package=dag_name)

    logger = setup_logging()
    doc_md = try_render_readme(dag_path)

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

    return dag_name, dag_helpers, sql_queries, doc_md, logger, local_tz, default_args


def get_dags():
    """Create a list of all DAG names registered to Airflow"""
    dags = []
    for dag in DagBag().dags.values():
        # add dag name to list
        dags.append(dag._dag_id)
        # logger.info(f"dag = {dag._dag_id}")

    return dags


def setup_logging():
    """Set up a specific logger with our desired output level"""
    logging.basicConfig(format="%(message)s")
    logger = logging.getLogger("airflow.task")
    logger.setLevel(logging.INFO)

    return logger


def try_render_readme(dag_path):
    """Attempt to render README file if it exists"""

    try:
        return open(os.path.join(dag_path, "README.md")).read()
    except FileNotFoundError:
        print("Error, cannot render README.md")
        return ""


def hello_world():
    """return 'hello world!'"""

    return "Hello world!"


def get_datetime():
    """Returns the current date time using the local timezone."""

    return pendulum.now(local_tz).strftime("%d-%m-%Y %H:%M:%S")
