# Usage:
# make installations	# install the package for the first time, managing dependencies & performing a housekeeping cleanup too
# make deps		# just install the dependencies
# make install		# perform the end-to-end install
# make clean		# perform a housekeeping cleanup

all: installations

.EXPORT_ALL_VARIABLES:
.PHONY = installations deps clean install get_ips validate_user_ip

CONFIG_FILE := ip/config.yaml
# the 2 vars below are just for formatting CLI message output
COLOUR_TXT_FMT_OPENING := \033[0;33m
COLOUR_TXT_FMT_CLOSING := \033[0m

installations: clean deps install

deps: get_ips
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'deps'. Download the relevant pip package dependencies (note: ignore the pip depedency resolver errors.)${COLOUR_TXT_FMT_CLOSING}"
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@make -s clean
	@virtualenv -p python3 venv; \
	source venv/bin/activate; \
	pip3 install -r requirements.txt; \

############################################################################################
# Setup/validation targets: 'get_ips'
#############################################################################################
get_ips:
	@# Target: 'get_ips'. Get input args from config.yaml
	$(eval AIRFLOW_HOME_DIR=$(shell yq '.airflow_args.airflow_home_dir | select( . != null )' ${CONFIG_FILE}))
	$(eval ADMIN_PASS=$(shell yq '.airflow_args.admin_pass | select( . != null )' ${CONFIG_FILE}))
	$(eval USER_DEMO_PASS=$(shell yq '.airflow_args.user_demo_pass | select( . != null )' ${CONFIG_FILE}))

validate_user_ip: get_ips
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'validate_user_ip'. Validate the user inputs.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	# INFO: Verify the user has provided a value for the key 'AIRFLOW_HOME_DIR' in ip/config.yaml
	@[ "${AIRFLOW_HOME_DIR}" ] || ( echo "\nError: 'AIRFLOW_HOME_DIR' key is empty in ip/config.yaml\n"; exit 1 )

install: get_ips
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'install'. Run the setup and install targets.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	# remove the previously generated venv
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING} Previous installs of Airflow can conflict the metadata db, so reset the metadata just in case.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@airflow db reset
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING} Initialize the airflow db.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@airflow db init
	@sleep 10
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING} Copy over the predefined airflow config.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@cp ip/airflow.cfg	$(subst $\",,$(AIRFLOW_HOME_DIR))
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING} Create an Airflow admin user.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@make -s create_admin_user
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING} Create example 'read-only' and 'creator' users.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@make -s create_ro_user_example
	@make -s create_creator_user_example
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING} Start the airflow scheduler & webserver using a daemon process (i.e., the -D option).${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@airflow webserver -D
	@airflow scheduler -D
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING} Finished! Open up localhost:8080 in a web browser and use the admin account just created to login.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"

#############################################################################################
# Airflow-specific targets
#############################################################################################
# The two targets below are called by the above install target
create_admin_user: get_ips
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'create_admin_user'. Create an admin user for Airflow.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@airflow users create \
		--username pfry \
		--password ${ADMIN_PASS} \
		--firstname Peter \
		--lastname Parker \
		--role Admin \
		--email spiderman@superhero.org

create_ro_user_example: get_ips
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'create_ro_user_example'. Create user & assign them the 'user' role in Airflow.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@airflow users create \
		--username read_only_demo \
		--password ${USER_DEMO_PASS} \
		--firstname read_only_demo \
		--lastname read_only_demo \
		--role Viewer \
		--email read_only_demo@test.com

create_creator_user_example: get_ips
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'create_creator_user_example'. Create user & assign them the 'user' role in Airflow.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@airflow users create \
		--username creator_demo \
		--password ${USER_DEMO_PASS} \
		--firstname creator_demo \
		--lastname creator_demo \
		--role User \
		--email creator_demo@test.com

create_custom_role_example:
	curl -X POST http://localhost:8080/api/v1/roles \
	-H "Content-Type: application/json" \
	--user "pfry:${ADMIN_PASS}" \
	-d "{\"name\":\"read_only_role\", \"actions\":[{\"action\":{\"name\":\"can_read\"},\"resource\":{\"name\":\"DAGs\"}}]}"

add_user_to_role:
	airflow users add-role -u pfry -r read_only_role

#############################################################################################
# Custom-Airflow targets
#############################################################################################
trigger_dag:
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'trigger_dag'. Trigger an Airflow DAG.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	$(info [+] Trigger an Airflow DAG)
	@airflow dags trigger dbt_dag

trigger_dag_w_ip:
	$(info [+] Trigger an Airflow DAG with input provided)
	@airflow dags trigger template_dms_task_dag --conf '{"dms_task_name":"example-task"}'

#############################################################################################
# Drop Airflow instance
#############################################################################################
debug:
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'debug'. Use this if you need to reinstall airflow.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@sudo rm -rf ${AIRFLOW_HOME}

kill_af_scheduler_and_webserver:
	# find the (Airflow) process pids and (manually) kill them
	#@lsof -i tcp:8080
	@# kill the relevant pid

clean:
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target 'clean'. Remove any redundant files, e.g. downloads.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
	@rm -rf ./venv
