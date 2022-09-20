# from airflow.util.dag_defaults import *
from airflow.operators.snowflake_operator import SnowflakeOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.models.dagbag import DagBag
from airflow.clients.snowflake_client import Snowflake
import pandas as pd

dagpath, dagname, dagroot, helpers, queries, templates = setup_dag(__file__)

dag = get_dag_object(__file__)  # TODO - change

task_flds = ["task_id", "_upstream_task_ids", "_downstream_task_ids", "parameters", "warehouse", "database", "role", "schema", "template", "function"]

parameter_flds = ["target", "dataset_id", "sql"]


def parse_task_meta(meta):
    flds = task_flds
    if "parameters" in flds and "parameters" in meta.keys():
        params = meta.pop("parameters")
        meta = {**meta, **params}
        return {k: v for k, v in meta.items() if k in task_flds + parameter_flds}
    return {k: v for k, v in meta.items() if k in flds}


def dags_iter():
    for path in os.scandir(dagroot):
        if path.is_dir():
            if os.path.exists(os.path.join(path, "dag.py")):
                yield path.name


def parse_df(df):
    list_like_flds = ["_upstream_task_ids", "_downstream_task_ids"]
    for fld in list_like_flds:
        if fld in df.columns:
            df[fld] = df[fld].map(lambda x: x if pd.isnull(x) else str(list(x)).replace("[", "").replace("]", "").replace("'", ""))

    if "function" in df.columns:
        df["function"] = df["function"].map(lambda x: x if pd.isnull(x) else x.__name__)
    return df


def get_meta():
    rows = []
    for dag_id in dags_iter():
        print("Checking DAG", dag_id)
        d = DagBag().get_dag(dag_id)
        try:
            print(d.__dict__)
            for task_name, task in d.__dict__["task_dict"].items():
                print("Parsing task", task_name)
                task_meta = d.__dict__["task_dict"][task_name].__dict__
                task_meta = parse_task_meta(task_meta)
                task_meta["dag_id"] = dag_id
                print(task_meta)
                rows.append(task_meta)
        except Exception as e:
            rows.append({"dag_id": dag_id, "error_dag_parsing": True})
            continue
    df = pd.DataFrame(rows)
    print(df)
    print(df.info())
    print("Trying to save table to snowflake...")
    df = parse_df(df)
    print(df)
    print(df.info())
    Snowflake(env=env).save_table(df, table="dag_task_meta", schema="cleaned")


start_task = DummyOperator(task_id="start", dag=dag)
end_task = DummyOperator(task_id="end", dag=dag)

start_task >> PythonOperator(task_id="get_meta", python_callable=get_meta) >> end_task
