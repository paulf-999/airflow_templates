#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : unit_tests.py
* Description   : Boilerplate Airflow pytest script
* Created       : 13-12-2021
* Usage         : pytest tests/unit_tests.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import pytest
from airflow.models import DagBag

# TODO: load equivalent 'src' files
# from src.boilerplate import is_even

# TODO: delete this func
# def test_valid_even():
# 	assert is_even(2)

dag_name = "example_dag"


@pytest.fixture()
def dagbag():
    return DagBag()


def test_dag_loaded(dagbag):
    dag = dagbag.get_dag(dag_id="hello_world")
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 1
