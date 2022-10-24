# (Airflow) Includes

The 'includes' folder acts as a Python package for our Airflow code and is used to store common/reusable code in a shared place to our code DRY and improve code readability.

To create/use a 'shared' Airflow modules folder:

1. Create an `includes` folder at the same level as your DAGs
2. Inside the 'includes folder:
  * Create a python script inside the folder to contain your reusable code, e.g., `common.py`
  * Create an empty file called '__init__.py` to indicate to Python that the directory should be treated as a package
3. In your Airflow DAG, import this 'common' package by importing it at the top of your script:

`from includes import common`
