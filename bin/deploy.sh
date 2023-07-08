echo "\n>>> INSTALLING PYTHON USING RTX...\n"
rtx install python

echo "\n>>> INSTALLING POETRY DEPENDENCIES...\n"
poetry install
echo "\n>>> GENERATING REQUIREMENTS.TXT FILE...\n"
poetry export > src/requirements.txt

echo "\n>>> BUILDING SAM TEMPLATE...\n"
sam build
echo "\n>>> DEPLOYING SAM TEMPLATE...\n"
sam deploy --stack-name gql-sqs-subscription --resolve-s3 --s3-prefix gql-sqs-subscription --capabilities CAPABILITY_NAMED_IAM --profile ggs-scarrera --no-confirm-changeset