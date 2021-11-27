import os
import logging
from datetime import datetime
from time import time
from airflow.models import dagrun
import pendulum
import humanfriendly
from airflow.operators.python import get_current_context
from airflow.models.dagbag import DagBag
from airflow.models.dagrun import DagRun
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
import snowflake.connector

# TODO
# add routine to also update 'AIRFLOW_DAG' table, for 'last_schedule_run' and 'next_schedule_run'

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

# capture TZ info
local_tz = pendulum.timezone("Australia/Melbourne")
utc_tz = pendulum.timezone("UTC")

sf_db = os.environ["BIKE_SHOP_RAW_DB"]
sf_schema = os.environ["BIKE_SHOP_SCHEMA"]

conn = snowflake.connector.connect(
    user=os.environ["BIKE_SHOP_DBT_USER"],
    password=os.environ["BIKE_SHOP_DBT_PASS"],
    account=os.environ["sf_acc_name_dbt_demo"],
    warehouse=os.environ["BIKE_SHOP_WH"],
    database=sf_db,
    schema=sf_schema,
)


def get_airflow_endpoints_and_ips_for_dag_runtime_stats():
    """Summary: Housekeeping function used to setup the required Airflow endpoints and setup the inputs required for the function 'get_dag_runtime_stats'

    Returns:
        payload: the JSON payload sent from the source ('triggering') Airflow dag
        src_dag_name: the name of the 'source' Airflow DAG, that triggered this 'get_dag_metadata_runtime_stats' dag
        dag_endpoint: the dag Airflow endpoint
        dag_runs_endpoint: the DAG endpoint, used to retrieve info about the DAG (and not the dag run)
        last_dagrun_run_id: the 'run_id' of the unique dag_run of the 'source' Airflow DAG
    """
    context = get_current_context()
    # payload was the input passed into this Airflow DAG
    payload = context["dag_run"].conf
    src_dag_name = payload["source_dag"]
    print(f"length of {payload} = {len(payload)}")

    logger.info(f"payload = {payload}")
    logger.info(f"src_dag_name = {payload['source_dag']}")

    # get the run_id of this dagrun
    dag_endpoint = DagBag().get_dag(src_dag_name)
    dag_runs_endpoint = DagRun.find(dag_id=src_dag_name)

    # with the run_id (var = last_dagrun_run_id), we can get: the state, the start/end time and the task details
    last_dagrun_run_id = dag_endpoint.get_last_dagrun(include_externally_triggered=True).execution_date
    logger.info(f"run_id = {last_dagrun_run_id}")

    return src_dag_name, dag_endpoint, dag_runs_endpoint, last_dagrun_run_id


def get_dag_runtime_stats(**kwargs):
    """Summary: Fetches DAG-level metadata for a given dagrun. For example:
    * The state of the dagrun
    * The start and endtime of the dagrun
    * and the tasks that make up the DAG
    """
    # get the inputs needed for this function (src_dag_name & last_dag_run_id)
    src_dag_name, dag_endpoint, dag_runs_endpoint, last_dagrun_run_id = get_airflow_endpoints_and_ips_for_dag_runtime_stats()

    # `runtime_stats_dict` is used to store the runtime stats. Will capture both the DAG & Task-level stats
    # This will need to be passed to a separate Airflow task
    runtime_stats_dict = {}
    runtime_stats_dict["dag_level_stats"] = {}
    runtime_stats_dict["dag_task_level_stats"] = {}

    cs = conn.cursor()

    for dag_run in dag_runs_endpoint:
        # get the dag_run details for the Airflow Dag that triggered this
        if dag_run.execution_date == last_dagrun_run_id:
            # cleanse the date fields to remove the timezone '+00' str
            start_date = datetime.strptime(str(dag_run.start_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            end_date = datetime.strptime(str(dag_run.end_date.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
            duration = end_date - start_date
            # with dag_run retrieved, you can then fetch the fields below
            runtime_stats_dict["dag_level_stats"]["dag_name"] = src_dag_name
            runtime_stats_dict["dag_level_stats"]["dag_schedule_interval"] = dag_endpoint.schedule_interval
            runtime_stats_dict["dag_level_stats"]["dag_run"] = str(dag_run.run_id)
            runtime_stats_dict["dag_level_stats"]["dag_run_state"] = dag_run.state
            runtime_stats_dict["dag_level_stats"]["dag_run_start_date"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
            runtime_stats_dict["dag_level_stats"]["dag_run_end_date"] = end_date.strftime("%Y-%m-%d %H:%M:%S")
            runtime_stats_dict["dag_level_stats"]["dag_run_duration"] = humanfriendly.format_timespan(duration)
            logger.info("####################################################################")
            logger.info("DAG-level runtime metadata")
            logger.info("####################################################################")

            # write out the dict contents (for the DAG-level stats) to the terminal
            for key, value in runtime_stats_dict.items():
                if type(value) is dict and key == "dag_level_stats":
                    for child_key, child_value in value.items():
                        logger.info(f"{child_key} = {child_value}")

            logger.info("####################################################################")
            logger.info("TASK-level runtime metadata")
            logger.info("####################################################################")
            # now retrieve the corresponding Airflow tasks & their metadata
            dag_run_tasks = dag_run.get_task_instances()

            for task in dag_run_tasks:
                runtime_stats_dict["dag_task_level_stats"]["task_name"] = task.task_id
                runtime_stats_dict["dag_task_level_stats"]["task_state"] = task.state
                runtime_stats_dict["dag_task_level_stats"]["task_start_date"] = fmt_airflow_dt_vals(task.start_date)
                runtime_stats_dict["dag_task_level_stats"]["task_end_date"] = fmt_airflow_dt_vals(task.end_date)
                runtime_stats_dict["dag_task_level_stats"]["task_duration"] = humanfriendly.format_timespan(task.duration)

                # write out the dict contents (for the TASK-level stats) to the terminal
                for key, value in runtime_stats_dict.items():
                    if type(value) is dict and key == "dag_task_level_stats":
                        for child_key, child_value in value.items():
                            logger.info(f"{child_key} = {child_value}")

                            # Insert the data into the Snowflake table!
                            cs.execute(
                                f"INSERT INTO {sf_db}.{sf_schema}.AIRFLOW_DAG_RUN (DAG_NAME, DAG_RUN, DAG_RUN_STATE, DAG_RUN_START_DATE, DAG_RUN_END_DATE, DAG_RUN_DURATION, DAG_RUN_TASK_NAME, DAG_RUN_TASK_STATE, DAG_RUN_TASK_START_DATE, DAG_RUN_TASK_END_DATE, DAG_RUN_TASK_DURATION, QUERY_TS) VALUES ('{runtime_stats_dict['dag_level_stats']['dag_name']}', '{runtime_stats_dict['dag_level_stats']['dag_run']}', '{runtime_stats_dict['dag_level_stats']['dag_run_state']}', '{runtime_stats_dict['dag_level_stats']['dag_run_start_date']}', '{runtime_stats_dict['dag_level_stats']['dag_run_end_date']}', '{runtime_stats_dict['dag_level_stats']['dag_run_duration']}','{runtime_stats_dict['dag_task_level_stats']['task_name']}', '{runtime_stats_dict['dag_task_level_stats']['task_state']}', '{runtime_stats_dict['dag_task_level_stats']['task_start_date']}', '{runtime_stats_dict['dag_task_level_stats']['task_end_date']}', '{runtime_stats_dict['dag_task_level_stats']['task_duration']}', current_timestamp());"
                            )

                logger.info("###########################################")
        else:
            logger.debug("dag_run details not found!")
            logger.debug(f"dag_run = {dag_run}")
            logger.debug(f"dag_run.execution_date = {dag_run.execution_date}")
            logger.debug(f"last_dagrun_run_id = {last_dagrun_run_id}")

    conn.close()

    return runtime_stats_dict


def fmt_airflow_dt_vals(ip_dt_val):
    """Summary: the same date formatting is used repeatedly, thus this function has been created to improve readability.
    Args:
        ip_dt_val (string): Input date/time value, requiring formatting

    Returns:
        fmted_dt_val (string): Formatted date/time value
    """

    return datetime.strptime(str(ip_dt_val.astimezone(local_tz)).split("+")[0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")


def get_runtime_stats_dict(**kwargs):
    """
    Summary: read in runtime stats from dict obj in previous task

    Returns:
        Python dict: Stores the runtime metadata of the Airflow DAG
    """
    START_TIME = time()
    logger.debug("Function called: get_user_ips()")

    ti = kwargs["ti"]
    runtime_stats_dict = ti.xcom_pull(task_ids="get_dag_runtime_stats")

    print(f"runtime_stats_dict = {runtime_stats_dict}")

    """
    for key, value in runtime_stats_dict.items():
        if type(value) is dict and key == "dag_level_stats":
            for child_key, child_value in value.items():
                logger.info(f"{child_key} = {child_value}")

                cs = conn.cursor()
                try:
                    cs.execute(f"INSERT INTO {sf_db}.${sf_schema}.airflow_etl_control_tbl () ")
                    one_row = cs.fetchone()
                    print(one_row[0])
                finally:
                    cs.close()
                conn.close()
    """
    logger.debug(f"Function finished: read_op() finished in {round(time() - START_TIME, 2)} seconds")

    return runtime_stats_dict
