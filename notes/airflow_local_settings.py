from contextlib import contextmanager
import logging
from datetime import datetime

from airflow.models import BaseOperator
from pendulum import timezone, now

logging.basicConfig(format="%(message)s")
logger = logging.getLogger("application_logger")
logger.setLevel(logging.INFO)

local_tz = timezone("Australia/Melbourne")


def pre_duration(context):
    context["task_instance"].task._tracking_start_time = now(local_tz)


def post_duration(context, result):
    print(f"context = {context}")
    task = context["task_instance"].task
    duration = now() - task._tracking_start_time
    _tracking_end_time = now(local_tz)
    print("############################################################")

    print(f"dag = {context['dag']}")
    print(f"run_id = {context['run_id']}")
    print(f"task = {context['task_instance'].task.task_id}")
    print(f"owner = {context['task_instance'].task.owner}")
    print(f"task state = {context['task_instance'].state}")
    print(f"start time = {datetime.strftime(task._tracking_start_time, '%d-%m-%Y %H:%M:%S')}")
    print(f"end time = {datetime.strftime(_tracking_end_time, '%d-%m-%Y %H:%M:%S')}")
    print(f"task duration: {duration.in_words()}")
    print("############################################################")


def wrap(func, wrapper):
    def inner(*args, **kwargs):

        wrapper(*args, **kwargs)
        return func(*args, **kwargs)

    return inner


def add_policy(task, pre, post):
    task.pre_execute = wrap(task.pre_execute, pre)
    task.post_execute = wrap(task.post_execute, post)

    return task


def track_status(task):
    def report_failed(context):
        task_instance = context["task_instance"].task
        error = context["exception"]
        logger.error(f"task {task_instance.task_id} failed with {error}. " f"task state {task_instance.state}. " f"report to {task_instance.owner}.")

    task.on_failure_callback = wrap(task.on_failure_callback, report_failed)
    task.on_retry_callback = wrap(task.on_retry_callback, report_failed)
    return task


def task_policy(task: BaseOperator):
    task = add_policy(task, pre_duration, post_duration)
    task = track_status(task)
