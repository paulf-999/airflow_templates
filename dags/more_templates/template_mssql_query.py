#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : template_mssql_query.py
* Description   : Boilerplate MSSQL query script.
* Created       : 04-06-2021
* Usage         : python3 template_mssql_query.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
import logging
import pymssql
from time import time
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": days_ago(1)}


def mssql_query(**kwargs):
    """generic mssql query function"""
    START_TIME = time()
    logger.debug("Function called: mssql_query()")

    db_name, db_schema, ip_tbl_list, db_host, username, password = get_user_ips()

    # initialise the var
    query_result_to_return = ""
    sql_query = f"SELECT * FROM {db_name}.{db_schema}.{ip_tbl_list}"

    try:
        conn = pymssql.connect(server=f"{db_host}", user=f"{username}", password=f"{password}", database=f"{db_name}")

        # Create a cursor from the connection
        with conn.cursor() as cursor:
            logger.info(
                f"Running query: {sql_query}",
            )

            cursor.execute(sql_query)

            query_result = cursor.fetchall()
            for item in query_result:
                query_result_to_return += f"{item[1]}\n"

        logger.info("Finished SQL query")

    except:
        logger.error(
            f"Error when creating pymssql database connection: {sys.exc_info()[0]}",
        )

    logger.debug(f"Function finished: main() finished in {round(time() - START_TIME, 2)} seconds")

    return query_result_to_return


def get_user_ips():
    """fetch user inputs"""
    START_TIME = time()
    logger.debug("Function called: get_user_ips()")

    db_name = Variable.get("db_name")
    db_schema = Variable.get("db_schema")
    ip_tbl_list = Variable.get("ip_tbl_list")
    db_host = Variable.get("host")
    username = Variable.get("username")
    password = Variable.get("password")

    logger.debug(f"Function finished: get_user_ips() finished in {round(time() - START_TIME, 2)} seconds")

    return db_name, db_schema, ip_tbl_list, db_host, username, password


with DAG(dag_id=os.path.basename(__file__).replace(".py", ""), default_args=default_args, schedule_interval=None, tags=["python", "template"]) as dag:
    mssql_select_all_query = PythonOperator(task_id="mssql_select_all_query", python_callable=mssql_query)
