#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : mssql_query.py
* Description   : Boilerplate MSSQL query script.
* Created       : 04-06-2021
* Usage         : python3 mssql_query.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import sys
import logging
import pymssql
from time import time
from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

default_args = {
    'owner': 'aws',
    'depends_on_past': False,
    'start_date': datetime(2019, 2, 20),
    'provide_context': True
}

dag = DAG(
    'template_mssql_query', default_args=default_args, schedule_interval=None)

def mssql_query(**kwargs):
    """ generic mssql query function """
    START_TIME = time()
    logger.debug(f"Function called: mssql_query()")

    db_name, db_schema, ip_tbl_list, db_host, username, password = get_user_ips()

    query_result_to_return = ''
    sql_query = f"SELECT * FROM {db_name}.{db_schema}.{ip_tbl_list}"

    try:
        conn = pymssql.connect(
            server=f'{db_host}',
            user=f'{username}',
            password=f'{password}',
            database=f'{db_name}'
        )
        
        # Create a cursor from the connection
        with conn.cursor() as cursor:
            logger.info("running query: %s", sql_query)

            cursor.execute(sql_query)

            query_result = cursor.fetchall()
            for item in query_result:
                query_result_to_return += f"{item[1]}\n"

        logger.info("finished SQL query")

    except:
        logger.error("Error when creating pymssql database connection: %s", sys.exc_info()[0])

    logger.debug(f"Function finished: main() finished in {round(time() - START_TIME, 2)} seconds")

    return query_result_to_return

def get_user_ips():
    """ fetch user inputs """
    START_TIME = time()
    logger.debug(f"Function called: get_user_ips()")

    db_name = Variable.get("db_name")
    db_schema = Variable.get("db_schema")
    ip_tbl_list = Variable.get("ip_tbl_list")
    db_host = Variable.get("host")
    username = Variable.get("username")
    password = Variable.get("password")

    logger.debug(f"Function finished: get_user_ips() finished in {round(time() - START_TIME, 2)} seconds")

    return db_name, db_schema, ip_tbl_list, db_host, username, password

mssql_select_all_query = PythonOperator(
    task_id='mssql_select_all_query',
    python_callable=mssql_query,
    dag=dag
)
