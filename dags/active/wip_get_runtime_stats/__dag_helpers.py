import os
import logging
from datetime import datetime
import pendulum
import humanfriendly
from airflow.models.dagrun import DagRun
from airflow.models.dagbag import DagBag

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# capture TZ info
local_tz = pendulum.timezone("Australia/Melbourne")


def get_dags():
    dags = []
    for dag in DagBag().dags.values():
        dags.append(dag._dag_id)
        # print(f"dag = {dag._dag_id}")

    return dags


def get_dag_metadata(dag_name):

    dag = DagBag().get_dag(dag_name)
    schedule_interval = dag.schedule_interval

    return dag._dag_id, schedule_interval


def get_dag_run_metadata(dag_name):

    # get dag_runs
    print(dag_name)
    logger.info("------------------------------")
    logger.info("DAG-level details")
    dag_runs = DagRun.find(dag_id=dag_name)
    for dag_run in dag_runs:
        # print(f"dag_run = {dag_run}")
        # cleanse the date fields to remove the timezone '+00' str
        dag_run_start_date = fmt_airflow_dt_vals(dag_run.start_date)
        dag_run_end_date = fmt_airflow_dt_vals(dag_run.end_date)
        dag_run_duration = humanfriendly.format_timespan(dag_run_end_date - dag_run_start_date)
        dag_run_state = dag_run.state

        for x in [dag_run.run_id, dag_run_state, dag_run_duration]:
            print(x)

        print("##############################")

        get_dag_run_task_metadata(dag_run)


def get_dag_run_task_metadata(dag_run):

    logger.info("------------------------------")
    logger.info("Task-level details")

    dag_run_tasks = dag_run.get_task_instances()
    for task in dag_run_tasks:
        task_name = task.task_id
        task_state = task.state
        duration = humanfriendly.format_timespan(task.duration)

        for x in [task_name, task_state, duration]:
            print(x)
        print("##############################")

    return


def fmt_airflow_dt_vals(ip_dt_val):
    """
    Summary: the same date formatting is used repeatedly, thus this function has been created to improve readability.
    Args: ip_dt_val (string): Input date/time value, requiring formatting
    Returns: fmted_dt_val (string): Formatted date/time value
    """

    return datetime.strptime(str(ip_dt_val.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")


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
    except:
        print("Error, cannot render README.md")
        return ""
