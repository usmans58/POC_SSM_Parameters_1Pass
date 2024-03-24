import os
import boto3
import requests

# AWS credentials and region
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
eu_north_1 = 'eu-north-1'

# 1Password credentials and vault details
onepassword_token = os.getenv('1PASSWORD_API_TOKEN')
onepassword_vault_id = 'POC' 
onepassword_api_base_url = 'https://api.1password.com/v1'

# Initialize AWS SSM client
ssm_client = boto3.client('ssm', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=eu_north_1)

# Fetch parameters from AWS SSM Parameter Store by prefix
def fetch_parameters_by_prefix(prefix):
    parameters = {}
    response = ssm_client.get_parameters_by_path(
        Path='/',
        Recursive=True,
        WithDecryption=True
    )
    for param in response['Parameters']:
        parameters[param['Name']] = param['Value']
        print(f'Parameter Name: {param["Name"]}, Value: {param["Value"]}')
    return parameters

# Upload parameters to 1Password
def upload_parameters_to_1password(parameters):
    for key, value in parameters.items():
        item_data = {
            'vaultUuid': 'z6lgp2vnfmmlufbwlhstji53vm',
            'title': key,
            'fields': [
                {
                    'value': value,
                    'designation': 'password'
                }
            ]
        }
        headers = {
            'Authorization': f'Bearer {onepassword_token}',
            'Content-Type': 'application/json',
        }
        response = requests.post(f'{onepassword_api_base_url}/items', json=item_data, headers=headers)
        print(response)
        if response.status_code == 201:
            print(f'Successfully uploaded {key} to 1Password.')
        else:
            print(f'Failed to upload {key} to 1Password. Status code: {response.status_code}, Response: {response.text}')

if __name__ == "__main__":
    prefix = 'V8'
    parameters = fetch_parameters_by_prefix(prefix)
    print(parameters)
    upload_parameters_to_1password(parameters)
