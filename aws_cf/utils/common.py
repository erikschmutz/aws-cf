import boto3
import botocore.exceptions
import time
import subprocess
from .config import Config, Stack
from .context import Context
import tempfile
import json
import datetime

# 'StackStatus': 'CREATE_IN_PROGRESS'|'CREATE_FAILED'|'CREATE_COMPLETE'|'ROLLBACK_IN_PROGRESS'|'ROLLBACK_FAILED'|'ROLLBACK_COMPLETE'|'DELETE_IN_PROGRESS'|'DELETE_FAILED'|'DELETE_COMPLETE'|'UPDATE_IN_PROGRESS'|'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS'|'UPDATE_COMPLETE'|'UPDATE_FAILED'|'UPDATE_ROLLBACK_IN_PROGRESS'|'UPDATE_ROLLBACK_FAILED'|'UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS'|'UPDATE_ROLLBACK_COMPLETE'|'REVIEW_IN_PROGRESS'|'IMPORT_IN_PROGRESS'|'IMPORT_COMPLETE'|'IMPORT_ROLLBACK_IN_PROGRESS'|'IMPORT_ROLLBACK_FAILED'|'IMPORT_ROLLBACK_COMPLETE',

def create_change_set(stack: Stack, config: Config):
    PREFIX = Context.get_changeset_prefix()

    root_path = Context.get_root()

    path = stack.path
    path = path.replace("$root", root_path)
    client = boto3.client("cloudformation")
    name = stack.name
    change_set_name = PREFIX + str(datetime.datetime.now().isoformat()).replace(":", "").split(".")[0]

    try:
        client.list_change_sets(StackName=stack.name)
    except botocore.exceptions.ClientError as e:
        if str(e).endswith(f"Stack [{stack.name}] does not exist"):
            return None
        raise e

    parameters  =[]
    
    if stack.parameters:
        parameters = [{"ParameterKey": key, "ParameterValue": stack.parameters[key]} for key in stack.parameters.keys()]

    client.create_change_set(
        ChangeSetName=change_set_name,
        StackName=name,
        Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
        TemplateBody=package(stack, config),
        Parameters=parameters,
    )
    wait_for_ready(name, change_set_name)

    return client.describe_change_set(
        ChangeSetName=change_set_name,
        StackName=name
    )


def wait_for_status(name: str, status):

    client = boto3.client("cloudformation") 

    iterations = 0
    MAX_ITERATIONS = 300
    SLEEP_SECONDS = 5
    while True:
        time.sleep(SLEEP_SECONDS)
        response = client.describe_stacks(
           StackName=name,
        )

        stack = response["Stacks"][0]

        if iterations > MAX_ITERATIONS:
            raise Exception(f"Stack {name} took more than {MAX_ITERATIONS*SLEEP_SECONDS} seconds to deploy.")

        if stack["StackStatus"] not in status:
            break

        iterations += 1


def wait_for_stack_deployed(name: str):
    return wait_for_status(name, ['CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS'])

def wait_for_deleted(name: str):
    return wait_for_status(name, ['CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS'])

def wait_for_ready(name, change_set_name):
    client = boto3.client("cloudformation") 
    while True:
        response = client.describe_change_set(
            ChangeSetName=change_set_name,
            StackName=name,
        )
    
        response = client.describe_change_set(
            ChangeSetName=change_set_name,
            StackName=name,
        )

        if response["Status"] not in ["CREATE_PENDING", "CREATE_IN_PROGRESS"]:
            break

        time.sleep(3)

def remove_change_set(name: str, change_set_name: str):
    client = boto3.client("cloudformation")

    response = client.delete_change_set(
        ChangeSetName=change_set_name,
        StackName=name
    )

def format_diff(diff):
    action = diff["ResourceChange"]["Action"]
    resource_id = diff["ResourceChange"]["LogicalResourceId"]
    resource_type = diff["ResourceChange"]["ResourceType"]
    details = diff["ResourceChange"]["Details"]

    actionName = {
        "Add": "Adding",
        "Modify": "Modifying",
        "Remove": "Removing"
    }

    if len(details):
        return f"{actionName[action]} {resource_type} with id {resource_id} \n{json.dumps(details)}\n\n"
        
    return f"{actionName[action]} {resource_type} with id {resource_id}"

def deploy_stack(name: str, change_set):
    client = boto3.client("cloudformation")
    response = client.execute_change_set(
        ChangeSetName=change_set,
        StackName=name
    )
    wait_for_stack_deployed(name)

def create_stack(stack: Stack, template):
    client = boto3.client("cloudformation")
    parameters  =[]
    
    if stack.parameters:
        parameters = [{"ParameterKey": key, "ParameterValue": stack.parameters[key]} for key in stack.parameters.keys()]

    response = client.create_stack(
        StackName=stack.name,
        TemplateBody=template, 
        Capabilities=["CAPABILITY_NAMED_IAM", "CAPABILITY_AUTO_EXPAND"],
        Parameters=parameters
    )
    wait_for_stack_deployed(stack.name)

def delete_stack(name: str):
    client = boto3.client("cloudformation")
    client.delete_stack(
        StackName=name,
    )
    wait_for_deleted(name)

def package(stack: Stack, config: Config):
    args = [
            "aws", "cloudformation", "package",
            "--template", stack._path,
            "--s3-prefix", "aws/stacks",
            "--s3-bucket", config.enviroment.artifacts,
    ]
    
    if config.enviroment.profile:
        args.append("--profile")
        args.append(config.enviroment.profile)

    result = subprocess.check_output(args)
    return result.decode()

def get_yes_or_no(message):
    while True:
        result = input(message + " (enter y/n)")

        if result in ["yes", "y"]:
            return True

        if result in ["no", "n"]:
            return False