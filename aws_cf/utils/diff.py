from .common import wait_for_ready, get_yml
from .config import Config, Stack
import boto3
from pydantic import BaseModel
from typing import Any

class DiffResponse(BaseModel):
    new: bool
    changes: list[Any]

def create_change_set(name: str, path: str, root_path: str, config: Config):
    PREFIX = "AWSCF"

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

def get_differences(stack: Stack):
    pass