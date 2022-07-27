import os
import re
import pendulum
from airflow.operators.python import get_current_context

local_tz = pendulum.timezone("Australia/Melbourne")


def hello_world():
    """
    Description:
    Returns 'hello world!'.

    Args:
        kwargs: kwargs is used to capture multiple input vars
    """

    return "Hello world!"


def gen_metadata(**kwargs):

    print("########################################")
    context = get_current_context()
    ti = context["ti"]

    dag_id = re.sub("<DAG: |>", "", str(context["dag"]))
    run_id = context["run_id"]
    task_id = context["ti"].task_id
    job_id = context["ti"].job_id
    state = context["ti"].state
    dag_run = context["dag_run"]
    dag_run_start_date = context["dag_run"].start_date

    print(f"context = {context}")
    print(f"ti = {ti}")
    print(f"dag_run = {dag_run}")
    print("########################################")
    print(f"dag_id = {dag_id}")
    print(f"task_id = {task_id}")
    print(f"run_id = {run_id}")
    print(f"job_id = {job_id}")
    print(f"dag_run_start_date = {dag_run_start_date}")
    print("########################################")

    # return ",\n".join([f"{re.sub('[^a-zA-Z0-9]+','-',k)}={v}" for k, v in kwargs.items()])


def trigger(context, dag_run_obj):
    dag_run_obj.payload = {"message": context["dag_run"].conf["message"], "day": context["dag_run"].conf["day"]}
    return dag_run_obj


def get_datetime():
    """
    Description:
    Returns the current date time using the local timezone.

    Args:
        kwargs: kwargs is used to capture multiple input vars
    """

    return pendulum.now(local_tz).strftime("%d-%m-%Y %H:%M:%S")


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
    except Exception:
        print("Error, cannot render README.md")
        return ""
