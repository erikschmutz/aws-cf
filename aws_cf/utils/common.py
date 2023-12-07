import boto3
import time
import subprocess
from .config import Config
import tempfile

def get_yml(path, config, root_path):
    path = path.replace("$root", root_path)
    return package(open(path).read(), config)

def create_change_set(name: str, path: str, root_path: str, config: Config):
    PREFIX = "InfraScript"

    path = path.replace("$root", root_path)
    client = boto3.client("cloudformation")
    try:
        previouse_change_sets = client.list_change_sets(StackName=name)
    except:
        return None

    def get_name(previouse_change_sets):
        if not len(previouse_change_sets["Summaries"]):
            return PREFIX + "-" + name + "-" + str(1)

        previouse_name:str = previouse_change_sets["Summaries"][0]["ChangeSetName"]

        if not previouse_name.startswith(PREFIX):
            return PREFIX + "-" + name + "-" + str(1)

        previouse_index = int(previouse_name.split("-")[2])
        new_index = previouse_index + 1
        return PREFIX + name + "-" + str(new_index)

    change_set_name = get_name(previouse_change_sets)
    client.create_change_set(
        ChangeSetName=change_set_name,
        StackName=name,
        Capabilities=["CAPABILITY_NAMED_IAM"],
        TemplateBody=get_yml(path, config, root_path)
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
        TemplateBody=template
    )

def package(yml: str, config: Config):
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(bytes(yml, "utf-8"))
        tmp.read()
    
        result = subprocess.check_output(
            [
                "aws", "cloudformation", "package",
                "--template", tmp.name,
                "--s3-prefix", "aws/stacks",
                "--s3-bucket", config.Enviroments[0].artifacts,
                "--profile", config.Enviroments[0].profile
            ]
        )
        
        return result.decode()





def get_yes_or_no(message):
    while True:
        result = input(message + " (enter y/n)")

        if result in ["yes", "y"]:
            return True

        if result in ["no", "n"]:
            return True