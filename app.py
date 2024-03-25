import os
import time
import boto3
import onepasswordconnectsdk
from onepasswordconnectsdk.models import Field, GeneratorRecipe, Item,ItemVault



# AWS credentials and region
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
eu_north_1 = 'eu-north-1'

# 1Password credentials and vault details
op_connect_token = os.getenv("1PASSWORD_API_TOKEN")
default_vault = "POC"
connect_host = "https://my.1password.com/home"

client = onepasswordconnectsdk.client.new_client_from_environment(connect_host)



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
        user_item = Item(
            title= key,
            category= 'LOGIN',
            fields= [
                Field(
                    value= value,
                    purpose= 'PASSWORD'
                
                )  
            ]
        )
    posted_item = client.create_item(default_vault, user_item)
    time.sleep(5)


       

if __name__ == "__main__":
    prefix = 'V8'
    parameters = fetch_parameters_by_prefix(prefix)
    print(parameters.items())
    upload_parameters_to_1password(parameters)
