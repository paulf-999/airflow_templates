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


def get_dag_runtime_inputs():
    """
    Housekeeping function: used to setup the inputs required for the function 'get_dag_runtime_stats'

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
    # - the end time
    # - and the task details (WIP)

    return payload, src_dag_name, last_dagrun_run_id


def get_dag_runtime_stats(**kwargs):

    payload, src_dag_name, last_dagrun_run_id = get_dag_runtime_inputs()

    dag_runs = DagRun.find(dag_id=src_dag_name)

    for dag_run in dag_runs:
        # get the dag_run details for the Airflow Dag that triggered this
        if dag_run.execution_date == last_dagrun_run_id:
            # cleanse the date fields to remove the timezone '+00' str
            start_date = datetime.strptime(str(dag_run.start_date).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            end_date = datetime.strptime(str(dag_run.end_date).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            execution_date = datetime.strptime(str(dag_run.execution_date).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            duration = end_date - start_date
            logger.debug(f"dag_run = {dag_run}")
            # with dag_run retrieved, you can then fetch the fields below
            logger.info("####################################################################")
            logger.info("DAG-level runtime metadata")
            logger.info("####################################################################")
            logger.info(f"source dag name = {src_dag_name}")
            logger.info(f"dag_run.state = {dag_run.state}")
            logger.info(f"dag_run.execution_date = {execution_date}")
            logger.info(f"dag_run.start_date = {start_date}")
            logger.info(f"dag_run.end_date = {end_date}")
            logger.info(f"dag_run.duration = {humanfriendly.format_timespan(duration)}")
            logger.info("####################################################################")
        else:
            logger.info("dag_run details not found!")
            logger.debug(f"dag_run = {dag_run}")
            logger.debug(f"dag_run.execution_date = {dag_run.execution_date}")
            logger.info(f"last_dagrun_run_id = {last_dagrun_run_id}")
