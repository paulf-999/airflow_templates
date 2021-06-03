default: install_airflow

AIRFLOW_VERSION=2.0.1
PYTHON_VERSION=3.7
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.0.1/constraints-3.6.txt


install_airflow:
	pip install apache-airflow==${AIRFLOW_VERSION} --constraint ${CONSTRAINT_URL} -m .
	pip install apache-airflow-providers-microsoft-mssql --constraint "${CONSTRAINT_URL}"
	pip install apache-airflow-providers-amazon --constraint "${CONSTRAINT_URL}"
	pip install apache-airflow-providers-odbc --constraint "${CONSTRAINT_URL}"
	#pip install "apache-airflow[amazon,microsoft]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
	pip install smart-open==5.0.0 --constraint "${CONSTRAINT_URL}"

init_airflow_db:
	$(info [+] Initialize the airflow db)
	airflow db init

create_admin_user:
	airflow users create \
		--username pfry \
		--firstname Peter \
		--lastname Parker \
		--role Admin \
		--email spiderman@superhero.org

start_webserver:
	$(info [+] start the web server, default port is 8080)
	airflow webserver --port 8080

start_scheduler:
	$(info [+] start the scheduler)
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	airflow scheduler

# visit localhost:8080 in the browser and use the admin account you just
# created to login. Enable the example_bash_operator dag in the home page
