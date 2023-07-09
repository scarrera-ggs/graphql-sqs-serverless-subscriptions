#!/bin/bash

set -e
# The set -e option instructs bash to immediately exit if any command has a non-zero exit status.
# You wouldn't want to set this for your command-line shell, but in a script it's massively helpful. 
# In all widely used general-purpose programming languages, an unhandled runtime error

function usage() {
  cat <<EOF
Usage: $0 -c <config_file_path> -p <aws_profile> -r <aws_region> [OPTIONS]

Required parameters:
  -c, --config <config_file_path> The deployment configuration file path, i.e. 'deployments/<config_file>.toml
  -p, --profile <aws_profile>     The AWS profile to use
  -r, --region <aws_region>       The AWS region where the deployment take place, i.e. 'us-west-2 '

Optional parameters:
  -d, --debug                     Enable debug logging for this script
EOF
}

# Parse flag params
while [[ "$#" -gt 0 ]]; do
  case $1 in
  -c | --config)
    CONFIG_FILE="$2"
    shift
    ;;

  -p | --profile)
    AWS_PROFILE="$2"
    shift
    ;;

  -r | --region)
    AWS_REGION="$2"
    shift
    ;;

  -h | --help)
    usage
    exit
    ;;

  -d | --debug)
    DEBUG=1
    ;;

  *)
    echo "Unknown parameter passed: $1"
    exit 1
    ;;
  esac

  shift
done

# flag params validations
if [[ -z "${CONFIG_FILE}" ]] || [[ -z "${AWS_PROFILE}" ]] || [[ -z "${AWS_REGION}" ]]; then
  usage
  exit 1
fi

if [[ ! -e "${CONFIG_FILE}" ]]; then
  echo "Deployment configuration file ${CONFIG_FILE} not found."
  exit 1
fi

if [[ -n "$DEBUG" ]]; then
  set -x
fi

# deploy to aws
export AWS_PROFILE

rtx install python
poetry install
poetry export > src/requirements.txt

sam build --config-file "${CONFIG_FILE}"
sam deploy --resolve-s3 --config-file "${CONFIG_FILE}" --profile "${AWS_PROFILE}" --region "${AWS_REGION}"
