import os
import json
import boto3
from github import Github





# AWS credentials and region
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
eu_north_1 = 'eu-north-1'

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

def upload_parameters_to_repo(parameters):
    # Write parameters to JSON file
    with open('parameters.json', 'w') as json_file:
        json.dump(parameters, json_file, indent=4)

    # Commit JSON file to repository
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    main_branch = repo.get_branch("main")
    base_commit_sha = main_branch.commit.sha
    repo.create_file('parameters.json', 'Upload parameters to repository', json.dumps(parameters), branch='main', sha=base_commit_sha)
    print('Parameters uploaded to repository successfully.')

       

if __name__ == "__main__":
    prefix = 'V8'
    parameters = fetch_parameters_by_prefix(prefix)
    print(parameters.items())
    upload_parameters_to_repo(parameters)

