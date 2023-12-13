import boto3
import botocore.exceptions
import time
import subprocess
from .config import Config, Stack
from .context import Context
import tempfile
import json
import datetime


def create_change_set(stack: Stack, config: Config):
    PREFIX = Context.get_changeset_prefix()

    root_path = Context.get_root()

    path = stack.path
    path = path.replace("$root", root_path)
    client = boto3.client("cloudformation")
    name = stack.name
    change_set_name = PREFIX + str(datetime.datetime.now().isoformat()).replace(":", "-")
    
    parameters  =[]
    
    if stack.parameters:
        parameters = [{"ParameterKey": key, "ParameterValue": stack.parameters[key]} for key in stack.parameters.keys()]

    client.create_change_set(
        ChangeSetName=change_set_name,
        StackName=name,
        Capabilities=["CAPABILITY_NAMED_IAM"],
        TemplateBody=package(stack, config),
        Parameters=parameters,
    )
    wait_for_ready(name, change_set_name)

    return client.describe_change_set(
        ChangeSetName=change_set_name,
        StackName=name
    )


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

def create_stack(name: str, template:str):
    client = boto3.client("cloudformation")
    response = client.create_stack(
        StackName=name,
        TemplateBody=template, 
        Capabilities=["CAPABILITY_NAMED_IAM"],
    )

def package(stack: Stack, config: Config):
    args = [
            "aws", "cloudformation", "package",
            "--template", stack._path,
            "--s3-prefix", "aws/stacks",
            "--s3-bucket", config.Enviroments[0].artifacts,
    ]
    
    if config.Enviroments[0].profile:
        args.append("--profile")
        args.append(config.Enviroments[0].profile)

    result = subprocess.check_output(args)
    return result.decode()

def get_yes_or_no(message):
    while True:
        result = input(message + " (enter y/n)")

        if result in ["yes", "y"]:
            return True

        if result in ["no", "n"]:
            return True