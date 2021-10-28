import re
import json
import pendulum

local_tz = pendulum.timezone("Australia/Melbourne")


def hello_world(**kwargs):
    """
    Description:
    Returns 'hello world!'.

    Args:
        kwargs: kwargs is used to capture multiple input vars
    """

    return "Hello world!"


def gen_metadata(**kwargs):
    return ",\n".join([f"{re.sub('[^a-zA-Z0-9]+','-',k)}={v}" for k, v in kwargs.items()])


def get_datetime(**kwargs):
    """
    Description:
    Returns the current date time.

    Args:
        kwargs: kwargs is used to capture multiple input vars
    """

    return pendulum.now(local_tz).strftime("%d-%m-%Y %H:%M:%S")
