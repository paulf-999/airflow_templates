import logging
import os


def get_logger():
    """Set up a specific logger with our desired output level"""
    logging.basicConfig(format="%(message)s")
    logger = logging.getLogger("airflow.task")
    logger.setLevel(logging.INFO)

    return logger


def try_render_readme(dag_path):
    """Attempt to render README file if it exists"""

    try:
        return open(os.path.join(dag_path, "README.md")).read()
    except FileNotFoundError:
        print("Error, cannot render README.md")
        return ""


def hello_world():
    """return 'hello world!' Just used for testing purposes."""

    return "Hello world!"
