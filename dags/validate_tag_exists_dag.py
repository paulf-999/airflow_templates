from airflow.exceptions import AirflowClusterPolicyViolation
from airflow import DAG
from airflow.models.baseoperator import BaseOperator


def dag_policy(dag: DAG):
    """Ensure that DAG has at least one tag"""
    if not dag.tags:
        raise AirflowClusterPolicyViolation(f"DAG {dag.dag_id} has no tags. At least one tag required. File path: {dag.filepath}")
