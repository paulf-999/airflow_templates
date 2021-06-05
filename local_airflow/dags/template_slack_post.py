#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : template_slack_post.py
* Description   : Boilerplate slack post Airflow DAG script.
* Created       : 04-06-2021
* Usage         : python3 slack.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import logging
from airflow.models.dag import DAG
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format='%(message)s')
logger = logging.getLogger('airflow.task')
logger.setLevel(logging.INFO)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': days_ago(1)
}

slack_token = Variable.get("slack_token")

with DAG(
        dag_id='slack_test_dag',
        default_args=default_args,
        tags=['python','template']
    ) as dag:

    slack_test = SlackWebhookOperator(
        task_id='slack_message',
        http_conn_id='slack_connection',
        webhook_token=f'{slack_token}',
        message='Hello, World!',
        channel='#airflow-integration'
    )
    