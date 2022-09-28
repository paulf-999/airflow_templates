import os


def try_render_readme(dag_path):
    """Attempt to render README file if it exists"""

    try:
        return open(os.path.join(dag_path, "README.md")).read()
    except FileNotFoundError:
        print("Error, cannot render README.md")
        return ""


def hello_world():
    """return 'hello world!'"""

    return "Hello world!"
