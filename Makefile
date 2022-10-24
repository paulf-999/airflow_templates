# Usage:
# make installations	# install the package for the first time, managing dependencies & performing a housekeeping cleanup too
# make deps		# just install the dependencies
# make install		# perform the end-to-end install
# make clean		# perform a housekeeping cleanup

# all: deps install [X, Y, Z...] clean

.EXPORT_ALL_VARIABLES:
.PHONY = installations deps clean install get_ips validate_user_ip

CONFIG_FILE := ip/config.yaml
PIP_INSTALL_CMD=pip3 install -q --disable-pip-version-check

# the 2 vars below are just for formatting CLI message output
COLOUR_TXT_FMT_OPENING := \033[0;33m
COLOUR_TXT_FMT_CLOSING := \033[0m

installations: deps install clean

#############################################################################################
# Setup/validation targets: 'get_ips' & 'validate_user_ip'
#############################################################################################
deps: get_ips
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target: 'deps'. Download the relevant pip package dependencies (note: ignore the pip depedency resolver errors.)${COLOUR_TXT_FMT_CLOSING}"
	@echo "----------------------------------------------------------------------------------------------------------------------"
	@${PIP_INSTALL_CMD} -q -r requirements.txt

get_ips:
	@ Validate user input
	@make -s validate_user_ip
	@# Target: 'get_ips'. Get input args from config.yaml
	$(eval CURRENT_DIR=$(shell pwd))
	$(eval ENV=$(shell yq -r '.general_params.env | select( . != null )' ${CONFIG_FILE}))
	$(eval AIRFLOW_VERSION=$(shell jq '.airflow_args.airflow_version' ${CONFIG_FILE}))
	$(eval PYTHON_VERSION=$(shell jq '.airflow_args.python_version' ${CONFIG_FILE}))
	$(eval CONSTRAINT_URL=$(shell jq '.airflow_args.constraints_url' ${CONFIG_FILE}))
	$(eval AIRFLOW_HOME_DIR=$(shell jq '.airflow_args.airflow_home_dir' ${CONFIG_FILE}))

validate_user_ip: get_ips
	@echo "------------------------------------------------------------------"
	@echo "${COLOUR_TXT_FMT_OPENING}Target: 'validate_user_ip'. Validate the user inputs.${COLOUR_TXT_FMT_CLOSING}"
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

clean:
	@echo "------------------------------------------------------------------"
	@echo -e "${COLOUR_TXT_FMT_OPENING}Target 'clean'. Remove any redundant files, e.g. downloads.${COLOUR_TXT_FMT_CLOSING}"
	@echo "------------------------------------------------------------------"
