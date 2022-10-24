# Usage:
# make installations	# install the package for the first time, managing dependencies & performing a housekeeping cleanup too
# make deps		# just install the dependencies
# make install		# perform the end-to-end install
# make clean		# perform a housekeeping cleanup

all: installations

.EXPORT_ALL_VARIABLES:
.PHONY = installations deps clean install get_ips validate_user_ip

CONFIG_FILE := ip/config.yaml
PIP_INSTALL_CMD=pip3 install -q --disable-pip-version-check

# the 2 vars below are just for formatting CLI message output
COLOUR_TXT_FMT_OPENING := \033[0;33m
COLOUR_TXT_FMT_CLOSING := \033[0m

installations: deps install clean

deps: get_ips
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'deps'. Download the relevant pip package dependencies (note: ignore the pip depedency resolver errors.)${COLOUR_TXT_FMT_CLOSING}"
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@${PIP_INSTALL_CMD} -q -r requirements.txt
	@${PIP_INSTALL_CMD} apache-airflow==${AIRFLOW_VERSION}

############################################################################################
# Setup/validation targets: 'get_ips'
#############################################################################################
get_ips:
	@# Target: 'get_ips'. Get input args from config.yaml
	$(eval AIRFLOW_VERSION=$(shell yq '.airflow_args.airflow_version | select( . != null )' ${CONFIG_FILE}))
	$(eval PYTHON_VERSION=$(shell yq '.airflow_args.python_version | select( . != null )' ${CONFIG_FILE}))
	$(eval CONSTRAINT_URL=$(shell yq '.airflow_args.constraints_url | select( . != null )' ${CONFIG_FILE}))
	$(eval AIRFLOW_HOME_DIR=$(shell yq '.airflow_args.airflow_home_dir | select( . != null )' ${CONFIG_FILE}))

validate_user_ip: get_ips
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'validate_user_ip'. Validate the user inputs.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	# INFO: Verify the user has provided a value for the key 'env' in ip/config.yaml
	@[ "${ENV}" ] || ( echo "\nError: 'ENV' key is empty in ip/config.yaml\n"; exit 1 )
	# INFO: Verify the user has provided a value for the key 'AIRFLOW_VERSION' in ip/config.yaml
	@[ "${AIRFLOW_VERSION}" ] || ( echo "\nError: 'AIRFLOW_VERSION' key is empty in ip/config.yaml\n"; exit 1 )
	# INFO: Verify the user has provided a value for the key 'PYTHON_VERSION' in ip/config.yaml
	@[ "${PYTHON_VERSION}" ] || ( echo "\nError: 'PYTHON_VERSION' key is empty in ip/config.yaml\n"; exit 1 )
	# INFO: Verify the user has provided a value for the key 'CONSTRAINT_URL' in ip/config.yaml
	@[ "${CONSTRAINT_URL}" ] || ( echo "\nError: 'CONSTRAINT_URL' key is empty in ip/config.yaml\n"; exit 1 )
	# INFO: Verify the user has provided a value for the key 'AIRFLOW_HOME_DIR' in ip/config.yaml
	@[ "${AIRFLOW_HOME_DIR}" ] || ( echo "\nError: 'AIRFLOW_HOME_DIR' key is empty in ip/config.yaml\n"; exit 1 )

install: get_ips
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'install'. Run the setup and install targets.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	# Initialize the airflow db
	@airflow db init
	@sleep 10
	# copy over the predefined airflow config
	@cp ip/airflow.cfg	$(subst $\",,$(AIRFLOW_HOME_DIR))
	# Create the admin user
	@make create_admin_user
	# create example 'read-only' and 'creator' users
	@make create_ro_user_example
	@make create_creator_user_example
	# start the airflow scheduler & webserver
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	@airflow scheduler -D
	@airflow webserver --port 8080 -D
	# visit localhost:8080 in the browser and use the admin account just created to login

#############################################################################################
# Airflow-specific targets
#############################################################################################
# The two targets below are called by the above install target
create_admin_user:
	$(info [+] Create an admin user for Airflow)
	@airflow users create \
		--username pfry \
		--password ${adm_pass} \
		--firstname Peter \
		--lastname Parker \
		--role Admin \
		--email spiderman@superhero.org

create_ro_user_example:
	$(info [+] Create user & assign them the 'user' role in Airflow)
	@airflow users create \
		--username read_only_demo \
		--password ${user_demo_pass} \
		--firstname read_only_demo \
		--lastname read_only_demo \
		--role Viewer \
		--email read_only_demo@test.com

create_creator_user_example:
	$(info [+] Create user & assign them the 'user' role in Airflow)
	@airflow users create \
		--username creator_demo \
		--password ${user_demo_pass} \
		--firstname creator_demo \
		--lastname creator_demo \
		--role User \
		--email creator_demo@test.com

create_custom_role_example:
	curl -X POST http://localhost:8080/api/v1/roles \
	-H "Content-Type: application/json" \
	--user "pfry:${adm_pass}" \
	-d "{\"name\":\"read_only_role\", \"actions\":[{\"action\":{\"name\":\"can_read\"},\"resource\":{\"name\":\"DAGs\"}}]}"

add_user_to_role:
	airflow users add-role -u pfry -r read_only_role

#############################################################################################
# Custom-Airflow targets
#############################################################################################
trigger_dag:
	$(info [+] Trigger an Airflow DAG)
	@airflow dags trigger dbt_dag

trigger_dag_w_ip:
	$(info [+] Trigger an Airflow DAG with input provided)
	@airflow dags trigger template_dms_task_dag --conf '{"dms_task_name":"example-task"}'

#############################################################################################
# Drop Airflow instance
#############################################################################################
debug:
	# use this if you need to reinstall airflow
	@ rm -r ~/airflow/
	@ rm ~/airflow/airflow.db

kill_af_scheduler_and_webserver:
	# stop the Airflow scheduler & webserver
	@cat ~/airflow/airflow-scheduler.pid | xargs kill
	@cat ~/airflow/airflow-webserver.pid | xargs kill

clean:
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target 'clean'. Remove any redundant files, e.g. downloads.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
