SHELL = /bin/sh

#================================================================
# Usage
#================================================================
# make deps		# just install the dependencies
# make install		# perform the end-to-end install
# make clean		# perform a housekeeping cleanup

#=======================================================================
# Variables
#=======================================================================
.EXPORT_ALL_VARIABLES:

include src/make/variables.mk # load variables from a separate makefile file
include src/make/setup.mk # store setup targets in a separate makefile

ASTRO_PROJECT_NAME := dq_pipelines
SNOWFLAKE_CONNECTION_NAME := dm_snowflake_conn
#=======================================================================
# Targets
#=======================================================================
all: deps install clean

deps:
	@echo "${INFO}\nCalled makefile target 'deps'. Download any required libraries.${COLOUR_OFF}\n"
	@echo "${DEBUG}1. Download Astro CLI (note: you'll be asked for your unix password if you haven't recently provided it)${COLOUR_OFF}"
	@curl -sSL install.astronomer.io | sudo bash -s > /dev/null 2>&1
	@echo "${DEBUG}2. Generate template .env file${COLOUR_OFF}"
	@j2 ${JINJA_TEMPLATES_DIR}/.env_template.j2 -o .env && echo

install:
	@echo "${INFO}\nCalled makefile target 'install'. Run the setup & install targets.\n${COLOUR_OFF}"
	@make -s create_astro_project
	@make -s copy_generated_airflow_files
	@make -s generate_airflow_project_files

run:
	@echo "${INFO}\nCalled makefile target 'run'. Launch local Airflow instance using Astronomer.${COLOUR_OFF}\n"
	@make -s check_docker
	@echo "${DEBUG}Launch Airflow locally using Astronomer\n${COLOUR_OFF}"
	@# Start Astro. Note: an additional 5 minute allowance is added, to cater for the additional libs to be installed
	@cd ${ASTRO_PROJECT_NAME} && astro dev start --wait 5m

test:
	@echo "${INFO}\nCalled makefile target 'test'. Perform any required tests.${COLOUR_OFF}\n"

clean:
	@echo "${INFO}\nCalled makefile target 'clean'. Restoring the repository to its initial state.${COLOUR_OFF}\n"
	@rm -rf .env

# Phony targets
.PHONY: all deps install test clean

# .PHONY tells Make that these targets don't represent files
# This prevents conflicts with any files named "all" or "clean"
