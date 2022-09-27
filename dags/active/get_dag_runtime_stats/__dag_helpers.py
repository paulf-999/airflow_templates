import calendar
import logging
import os
from datetime import datetime

import humanfriendly
import pendulum
from airflow.models.dagbag import DagBag
from airflow.models.dagrun import DagRun

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# capture TZ info
local_tz = pendulum.timezone("Australia/Melbourne")


def get_dags():
    """Create a list of all DAG names registered to Airflow"""
    dags = []
    for dag in DagBag().dags.values():
        # add dag name to list
        dags.append(dag._dag_id)
        logger.info(f"dag = {dag._dag_id}")

    return dags


def get_dag_run_metadata(dag_name):
    """Get DAG-level dag_run metadata for a given DAG"""
    logger.info(f"DAG name: {dag_name}")
    logger.info("------------------------------")
    logger.info("dag_run details")
    logger.info("------------------------------")
    first_day_of_month, last_day_of_month = get_first_and_last_dates()
    # fmt: off
    dag_runs = DagRun.find(
        dag_id=dag_name,
        execution_start_date=first_day_of_month,
        execution_end_date=last_day_of_month
    )
    # fmt: on
    for dag_run in dag_runs:
        # cleanse the date fields to remove the timezone '+00' str
        dag_run_start_date = fmt_airflow_dt_vals(dag_run.start_date)
        dag_run_end_date = fmt_airflow_dt_vals(dag_run.end_date)
        dag_run_duration = humanfriendly.format_timespan(dag_run_end_date - dag_run_start_date)
        dag_run_state = dag_run.state
        # fmt: off
        list_pairs = [
            ("dag_run name", dag_run.run_id),
            ("dag_run state", dag_run_state),
            ("dag_run start date", dag_run_start_date),
            ("dag_run duration", dag_run_duration)
        ]
        # fmt: on

        for x in list_pairs:
            logger.info(f"{x[0]}: {x[1]}")

        # then get the task-level metadata
        get_dag_run_task_metadata(dag_run)


def get_dag_run_task_metadata(dag_run):
    """Get TASK-level dag_run metadata for a given DAG"""
    logger.info("------------------------------")
    logger.info("Task-level details")
    logger.info("------------------------------")

    dag_run_tasks = dag_run.get_task_instances()
    for task in dag_run_tasks:
        task_name = task.task_id
        task_state = task.state
        duration = humanfriendly.format_timespan(task.duration)

        # fmt: off
        list_pairs = [
            ("Task name", task_name),
            ("Task state", task_state),
            ("Task duration", duration)
        ]
        # fmt: on

        for x in list_pairs:
            logger.info(f"{x[0]}: {x[1]}")
        logger.info("------------------------------")

    return


def get_first_and_last_dates():
    """Get the first and last day of each month"""
    current_date = pendulum.now(local_tz)
    first_day_of_month = pendulum.datetime(current_date.year, current_date.month, 1)
    # fmt: off
    last_day_of_month = pendulum.datetime(
        current_date.year,
        current_date.month,
        calendar.monthrange(current_date.year, current_date.month)[1]
    )

    return first_day_of_month, last_day_of_month


def fmt_airflow_dt_vals(ip_dt_val):
    """Date formatting function to improve readability.
    Args: ip_dt_val (string): Input date/time value, requiring formatting.
    Returns: fmted_dt_val (string): Formatted date/time value
    """

    formatted_dt_value = str(ip_dt_val.astimezone(local_tz)).split("+")[0]

    return datetime.strptime(formatted_dt_value, "%Y-%m-%d %H:%M:%S.%f")


def try_render_readme(dag_path):
    """
    Returns "doc_md" parameter from dag_object_kwargs if it exists,
    otherwise tries to read README.md from "dagpath",
    otherwise fails silently and returns empty string.

    Parameters:
        dag_object_kwargs (dict): kwargs used to define DAG object
        dag_path (str): path for dag

    Returns:
        readme (str): Readme describing the dag
    """
    try:
        return open(os.path.join(dag_path, "README.md")).read()
    except FileNotFoundError:
        print("Error, cannot render README.md")
        return ""
