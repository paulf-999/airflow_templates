SHELL = /bin/sh

include .env # Load environment variables from .env file
include src/make/variables.mk # load variables from a separate file

TEMPLATES_DIR := src/templates
JINJA_TEMPLATES_DIR := ${TEMPLATES_DIR}/jinja_templates
#=======================================================================
# Targets
#=======================================================================
get_ips:
	@# Target: 'get_ips'. Get input args from config.yaml
	$(eval CURRENT_DIR=$(shell pwd))
	$(eval ENV=$(shell yq -r '.general_params.env | select( . != null )' ${CONFIG_FILE}))

validate_user_ip: get_ips
	@echo && echo "${INFO}Called makefile target 'validate_user_ip'. Validate the user inputs.${COLOUR_OFF}" && echo
	# verify the user has provided a value for the key 'env' in ip/config.yaml
	@[ "${ENV}" ] || ( echo "\nError: 'ENV' key is empty in ip/config.yaml\n"; exit 1 )

gen_env_template:
	@echo "${DEBUG}2. Generate template .env file${COLOUR_OFF}"
	@j2 ${JINJA_TEMPLATES_DIR}/.env_template.j2 -o .env && echo

validate_env_vars:
	@echo && echo "${INFO}Called makefile target 'validate_env_vars'. Verify the contents of required env vars.${COLOUR_OFF}" && echo
	@./src/sh/validate_env_vars.sh config.yaml .env

# Phony targets
.PHONY: get_ips validate_user_ip gen_env_template validate_env_vars
# .PHONY tells Make that these targets don't represent files
# This prevents conflicts with any files named "all" or "clean"
