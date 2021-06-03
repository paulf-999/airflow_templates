
import sys
import os
import logging
import pymssql
from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'aws',
    'depends_on_past': False,
    'start_date': datetime(2019, 2, 20),
    'provide_context': True
}

dag = DAG(
        dag_id=os.path.basename(__file__).replace(".py", ""),
        default_args=default_args,
        schedule_interval=None
)

def mssql_query(**kwargs):
    """ function to perform an MSSQL query """
    query_result_to_return = ''
    sql_query = ''

    try:
        conn = pymssql.connect(
            server=f'${HOST}',
            user=f'${USER}',
            password=f'${PWD}',
            database=f'${DB}'
        )
        
        # Create a cursor from the connection
        with conn.cursor() as cursor:
            logging.info("running query: %s", sql_query)

            cursor.execute(f"SELECT * from ${DB}.${schema}.${tbl}")

            query_result = cursor.fetchall()
            for item in query_result:
                query_result_to_return += f"{item[1]}\n"

        logging.info("Finished SQL query")

    except:
        logging.error("Error when creating pymssql database connection: %s", sys.exc_info()[0])

    logging.debug("Finished mssql_query() function in %s seconds", round(time() - START_TIME, 2))

    return query_result_to_return

select_query = PythonOperator(
    task_id='select_query',
    python_callable=mssql_query,
    dag=dag,
)
