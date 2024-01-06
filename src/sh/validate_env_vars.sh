#!/bin/bash
# shellcheck disable=all

#=======================================================================
# Variables
#=======================================================================
source .env # Load environment variables from .env file
source src/sh/common_script_vars.sh # fetch common shell script vars

# Path to the config.yaml file and .env file
CONFIG_FILE="$1"
ENV_FILE="$2"

ENV_VARS_TO_VALIDATE=("SNOWFLAKE_ACCOUNT" "SNOWFLAKE_USER" "SNOWFLAKE_PASSWORD" "SNOWFLAKE_DATABASE" "SNOWFLAKE_SCHEMA" "SNOWFLAKE_WAREHOUSE" "SNOWFLAKE_ROLE")
#=======================================================================
# Functions
#=======================================================================

# Function to validate the existance of an .env file
verify_env_file_exists() {
    if [ ! -f "$ENV_FILE" ]; then
        echo -e "${ERROR}Error: .env file not found.${COLOUR_OFF}"
        exit 1
    fi
}

# Function to verify that the required env vars have been populated in the .env file
validate_env_file() {
    for var in "${ENV_VARS_TO_VALIDATE[@]}"; do
        if [ -z "${!var}" ]; then
            echo && echo -e "${ERROR}Error: .env file error - '$var' is not populated in .env file.${COLOUR_OFF}" && echo
            exit 1
        fi
    done
}

# Function to verify that the required values in config.yaml have been populated
validate_config_yaml() {
    input_tables=$(sed -n -e '/^\s*- / { s/^\s*- //p }' "${CONFIG_FILE}")
    row_count_limit=$(sed -n -e 's/^\s*row_count_limit:\s*//p' "${CONFIG_FILE}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    gx_data_src_name=$(sed -n -e 's/^\s*gx_data_src_name:\s*//p' "${CONFIG_FILE}")

    # Debugging - uncomment if needed
    # display_extracted_values

    VALIDATED_VARIABLES=("input_tables" "row_count_limit" "gx_data_src_name")
    for var in "${VALIDATED_VARIABLES[@]}"; do
        value="${!var}"
        if [ -z "$value" ]; then
            echo -e "${ERROR}Error: config.yaml error - '$var' must not be empty in config.yaml.${COLOUR_OFF}" && echo
            exit 1
        fi
    done
}

# Function to echo extracted values
display_extracted_values() {
    config_file_vars=("input_tables" "row_count_limit" "gx_data_src_name")

    echo "Debuggging: extracted values from ${CONFIG_FILE}:" && echo
    for var in "${config_file_vars[@]}"; do
        value="${!var}"
        echo "$var: '$value'"
    done
}


#=======================================================================
# Main script logic
#=======================================================================

# Step 1: Verify .env file exists
echo -e "${DEBUG}* Check if .env file exists.${COLOUR_OFF}" && echo
verify_env_file_exists

# Step 2: validate .env file
echo -e "${DEBUG}* Validate contents of .env file.${COLOUR_OFF}"
validate_env_file
