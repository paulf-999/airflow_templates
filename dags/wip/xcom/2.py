# Import default libraries, setup logging, create common variables
from airflow_aac_v1.util.dag_defaults import *  # noqa - comment required to ignore linting warnings
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# Setup paths, import libraries and templates (seldom needs to change)
dagpath, dagname, dagroot, helpers, queries, templates = setup_dag(__file__)  # noqa

# Create the DAG object and add/override the any parameters. To add/override any params, just list these after the `__file__` variable. See the example below:
dag = get_dag_object(__file__, tags=["template", "dbt", "wip", "5"])  # noqa

dbt_project_dir = "/opt/airflow/dags/dbt/dbt_ofw"

# Create tasks
start_task = DummyOperator(task_id="start", dag=dag)
end_task = DummyOperator(task_id="end", dag=dag)

beep = "HERE"


def write_op():

    cmd = "debug"

    return cmd


# py_op_eg = PythonOperator(task_id="py_op_eg", python_callable=write_op)

# note: the jinja below needs to be escaped (i.e., double up every curly bracket), as an f-string is as used an input for the bash_command
bash_operator_eg = BashOperator(task_id="dbt_conn_test", bash_command=f"set -e; cd {dbt_project_dir}; dbt {{{{ dag_run.conf['src_tbl'] }}}} --profiles-dir profiles", dag=dag, retries=0)

# works
"""
bash_operator_eg = BashOperator(
    task_id="dbt_conn_test", bash_command="set -e; dbt debug --project-dir /opt/airflow/dags/dbt/dbt_ofw --profiles-dir /opt/airflow/dags/dbt/dbt_ofw/profiles", dag=dag, retries=0
)
"""

# works w/ip
"""
bash_operator_eg = BashOperator(
    task_id="dbt_conn_test", bash_command="set -e; cd /opt/airflow/dags/dbt/dbt_ofw; dbt {{ ti.xcom_pull(task_ids='py_op_eg') }} --profiles-dir profiles", dag=dag, retries=0
)
"""

# works w/ip & using an f-string (need to escape jinja)
"""
bash_operator_eg = BashOperator(task_id="dbt_conn_test", bash_command=f"set -e; cd {dbt_project_dir}; dbt {{{{ ti.xcom_pull(task_ids='py_op_eg') }}}} --profiles-dir profiles", dag=dag, retries=0)
"""

# works w/ip from xcom & f-string
"""
bash_operator_eg = BashOperator(
    task_id="dbt_conn_test", bash_command=f"echo \"here. {beep}. is the message: '$src_tbl'\"", env={"src_tbl": '{{ dag_run.conf["src_tbl"] if dag_run else "" }}'}, dag=dag, retries=0
)
"""

# BASELINED!
# bash_operator_eg = BashOperator(task_id="dbt_conn_test", bash_command=f"set -e; cd {dbt_project_dir}; dbt {{{{ dag_run.conf['src_tbl'] }}}} --profiles-dir profiles", dag=dag, retries=0)

# Create graph
# start_task >> py_op_eg >> bash_operator_eg >> end_task
start_task >> bash_operator_eg >> end_task
