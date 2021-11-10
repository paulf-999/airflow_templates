import re
from airflow.models import dagrun
import pendulum
from airflow.operators.python import get_current_context
from airflow.models.dagbag import DagBag
from airflow.models.dagrun import DagRun
from datetime import datetime

local_tz = pendulum.timezone("Australia/Melbourne")
utc_tz = pendulum.timezone("UTC")


def get_dagrun_deets():
    dag_bag = DagBag()
    dag = dag_bag.get_dag("template_dag")

    # get the run_id of this dagrun
    last_dagrun = dag.get_last_dagrun(include_externally_triggered=True).execution_date

    # with the run_id, we can get:
    # - the state
    # - the end time
    # - and the task details

    print(f"last_dagrun = {last_dagrun}")

    dag_id = "template_dag"
    dag_runs = DagRun.find(dag_id=dag_id)
    for dag_run in dag_runs:
        if dag_run.execution_date == last_dagrun:

            print(f"dag_run = {dag_run}")
            print(f"dag_run.state = {dag_run.state}")
            print(f"dag_run.execution_date = {dag_run.execution_date}")
            print(f"dag_run.start_date = {dag_run.start_date}")
            print(f"dag_run.end_date = {dag_run.end_date}")

            # dt = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")

            start_date = datetime.strptime(str(dag_run.start_date).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            end_date = datetime.strptime(str(dag_run.end_date).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            print(f"start_date = {start_date}")
            print(f"end_date = {end_date}")

            duration = end_date - start_date

            print(f"duration = {duration}")
            # print(duration.in_words())
            print(f"duration = {duration(duration).in_words()}")


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
