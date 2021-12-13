# ref: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#unit-tests

import pytest
from airflow.models import DagBag

# Fixtures are used when we want to run some code before every test method.
# So instead of repeating the same code in every test we define fixtures.
@pytest.fixture()
def dagbag():
    return DagBag()


def test_dag_loaded(dagbag, pytestconfig):
    dag = dagbag.get_dag(dag_id=pytestconfig.getoption("dag_name"))
    assert dagbag.import_errors == {}
    assert dag is not None
    # assert len(dag.tasks) == 1
