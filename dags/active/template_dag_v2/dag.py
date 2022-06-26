from include.common import *  # noqa

# fetch common variables from shared python module
dag_name, helpers, queries = get_common_dag_vars(__file__)  # noqa

with DAG(dag_id=dag_name, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:  # noqa

    ####################################################################
    # DAG Operators
    ####################################################################

    # separator tasks
    start_task = DummyOperator(task_id="start", dag=dag)  # noqa
    end_task = DummyOperator(task_id="end", dag=dag)  # noqa

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=helpers.hello_world)  # noqa

####################################################################
# DAG Lineage
####################################################################
start_task >> hello_world_task >> end_task

if __name__ == "__main__":
    """This is executed when run from the command line"""

    helpers.hello_world()
