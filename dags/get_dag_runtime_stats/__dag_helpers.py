import logging
from airflow.models import dagrun
import pendulum
import humanfriendly
from airflow.operators.python import get_current_context
from airflow.models.dagbag import DagBag
from airflow.models.dagrun import DagRun
from datetime import datetime

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# capture TZ info
local_tz = pendulum.timezone("Australia/Melbourne")
utc_tz = pendulum.timezone("UTC")


def get_inputs_for_dag_runtime_stats():
    """
    Summary: Housekeeping function: used to setup the inputs required for the function 'get_dag_runtime_stats'

    Returns:
        src_dag_name: the name of the 'source' Airflow DAG, that triggered this 'get_dag_metadata_runtime_stats' dag
        last_dagrun_run_id: the 'run_id' of the unique dag_run of the 'source' Airflow DAG
    """
    # instantiate objs
    dag_bag = DagBag()
    context = get_current_context()
    # instantiate vars - payload was the input passed into this Airflow DAG
    payload = context["dag_run"].conf
    src_dag_name = payload["source_dag"]

    logger.debug(f"payload = {payload}")
    logger.debug(f"src_dag_name = {payload['source_dag']}")

    # get the run_id of this dagrun
    last_dagrun_run_id = dag_bag.get_dag(src_dag_name).get_last_dagrun(include_externally_triggered=True).execution_date
    logger.debug(f"run_id = {last_dagrun_run_id}")

    # with the run_id (var = last_dagrun_run_id), we can get:
    # - the state
    # - the start and end time
    # - and the task details (WIP)

    return payload, src_dag_name, last_dagrun_run_id


def get_dag_runtime_stats(**kwargs):
    """
    Summary: Fetches DAG-level metadata for a given dagrun. For example:
    * The state of the dagrun
    * The start and endtime of the dagrun
    * and the tasks that make up the DAG (in progress)
    """
    # get the inputs needed for this function (src_dag_name & last_dag_run_id)
    payload, src_dag_name, last_dagrun_run_id = get_inputs_for_dag_runtime_stats()

    dag_runs = DagRun.find(dag_id=src_dag_name)

    for dag_run in dag_runs:
        # get the dag_run details for the Airflow Dag that triggered this
        if dag_run.execution_date == last_dagrun_run_id:
            # cleanse the date fields to remove the timezone '+00' str
            start_date = datetime.strptime(str(dag_run.start_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            end_date = datetime.strptime(str(dag_run.end_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            execution_date = datetime.strptime(str(dag_run.execution_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
            duration = end_date - start_date
            logger.info(f"dag_run = {dag_run}")
            # with dag_run retrieved, you can then fetch the fields below
            logger.info("####################################################################")
            logger.info("DAG-level runtime metadata")
            logger.info("####################################################################")
            logger.info(f"source dag name = {src_dag_name}")
            logger.info(f"dag_run.state = {dag_run.state}")
            logger.info(f"dag_run.execution_date = {execution_date}")
            logger.info(f"dag_run.start_date = {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"dag_run.end_date = {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"dag_run.duration = {humanfriendly.format_timespan(duration)}")
            logger.info("####################################################################")
            logger.info("TASK-level runtime metadata")
            logger.info("####################################################################")
            dag_run_tasks = dag_run.get_task_instances()
            for task in dag_run_tasks:
                logger.info(f"dag_run_task = {task}")
                logger.info(f"task.name = {task.task_id}")
                logger.info(f"task.state = {task.state}")
                task_execution_date = datetime.strptime(str(task.execution_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
                task_start_date = datetime.strptime(str(task.start_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
                task_end_date = datetime.strptime(str(task.end_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"task.execution_date = {task_execution_date}")
                logger.info(f"task.start_date = {task_start_date}")
                logger.info(f"task.end_date = {task_end_date}")
                logger.info(f"task.duration = {humanfriendly.format_timespan(task.duration)}")
                logger.info("###########################################")
        else:
            logger.debug("dag_run details not found!")
            logger.debug(f"dag_run = {dag_run}")
            logger.debug(f"dag_run.execution_date = {dag_run.execution_date}")
            logger.debug(f"last_dagrun_run_id = {last_dagrun_run_id}")

    return
