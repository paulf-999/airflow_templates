import os


def try_render_readme(dag_path):
    """
    Returns "doc_md" parameter from dag_object_kwargs if it exists,
    otherwise tries to read README.md from "dagpath",
    otherwise fails silently and returns empty string.

    Parameters:
        dag_object_kwargs (dict): kwargs used to define DAG object
        dag_path (str): path for dag

    Returns:
        readme (str): Readme describing the dag
    """
    try:
        return open(os.path.join(dag_path, "README.md")).read()
    except Exception:
        print("Error, cannot render README.md")
        return ""
