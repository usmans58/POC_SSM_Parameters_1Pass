import os
import json
import boto3
from onepassword_sdk import API
from onepassword_sdk.enums import VaultItemType

# AWS credentials and region
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
eu_north_1 = 'eu-north-1'

# 1Password credentials and vault details
onepassword_token = os.getenv('1PASSWORD_API_TOKEN')
onepassword_vault_id = 'your_vault_id'
item_type = VaultItemType.LOGIN

# Initialize AWS SSM client
ssm_client = boto3.client('ssm', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=eu_north_1)

# Fetch parameters from AWS SSM Parameter Store by prefix
def fetch_parameters_by_prefix(prefix):
    parameters = {}
    response = ssm_client.get_parameters_by_path(
        Path='/' + prefix,
        Recursive=True,
        WithDecryption=True
    )
    for param in response['Parameters']:
        parameters[param['Name']] = param['Value']
    return parameters

# Initialize 1Password API client
onepassword_api = API('your_domain.1password.com', onepassword_token)

# Upload parameters to 1Password
def upload_parameters_to_1password(parameters):
    for key, value in parameters.items():
        item = onepassword_api.create_item(onepassword_vault_id, item_type)
        item.title = key
        item.fields.append({
            'value': value,
            'name': 'password'
        })
        item.save()

if __name__ == "__main__":
    prefix = 'V8'
    parameters = fetch_parameters_by_prefix(prefix)
    print(parameters)
    upload_parameters_to_1password(parameters)
