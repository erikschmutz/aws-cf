from ..utils.logging import logger
from ..utils.config import Config
from ..utils.context import Context
import sys
from ..utils.common import create_change_set,package,tab, remove_change_set, format_diff,format_diffs
import re
import json 
import boto3
import time
import yaml
import os

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
green = "\x1b[32;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"
format = "%(message)s"

def add_color(node, color):
    keys = node.keys() if isinstance(node, dict) else range(len(node))

    for key in keys:
        item = node[key]

        if isinstance(item, list):
            add_color(item, color)
        elif isinstance(item, dict):
            add_color(item, color)
        else:
            print(f"<{color}>{item}</{color}>")
            node[key] = f"<{color}>{item}</{color}>"

    return node

def apply_colors(text: str):
    out = ""
    for line in text.split("\n"):
        out += line.replace("$GREEN$", green) 
        out += reset
        out += "\n"
    return out
class YAMLColor(yaml.YAMLObject):
    yaml_tag = u'!Color'

    def __init__(self, env_var):
        self.env_var = env_var

    @classmethod
    def to_yaml(cls, dumper, data):
        data.env_var = add_color(data.env_var, "green")
        return data

def detect_drift(stack_name, config):
    print(f"Detecting drift for {stack_name}...")

    client = boto3.client("cloudformation") 
    response = client.detect_stack_drift(
        StackName=stack_name
    )

    stack_drift_detection_id = response["StackDriftDetectionId"]

    iterations = 0
    MAX_ITERATIONS = 300
    SLEEP_SECONDS = 5

    while True:
        time.sleep(SLEEP_SECONDS)
        stack = client.describe_stack_drift_detection_status(
            StackDriftDetectionId=stack_drift_detection_id
        )


        if iterations > MAX_ITERATIONS:
            raise Exception(f"Stack {stack_name} took more than {MAX_ITERATIONS*SLEEP_SECONDS} seconds to deploy.")

        if stack["DetectionStatus"] == 'DETECTION_FAILED':
            raise Exception(f"Creating drift failed for stack {stack_name}...")

        if stack["DetectionStatus"] != 'DETECTION_IN_PROGRESS':
            break


        iterations += 1


    response = client.describe_stack_resource_drifts(
        StackName=stack_name,
        StackResourceDriftStatusFilters=[
            'MODIFIED'
        ],
    )

    stack = client.get_template(
        StackName=stack_name
    )

    def set_value_by_path(path: str, target, value):
        *path, last = path[1:].split("/")
        curr = target

        for p in path:
            if isinstance(target, list):
                curr = curr[int(p)]
            else:
                curr = curr.get(p)


        if isinstance(curr, list):
            curr.insert(int(last) + 1, value)
        else:
            curr[last] = value

        return target

    def format_value(node, prefix):
        if isinstance(node, str):
            return prefix + node
        print("node", node)
        keys = node.keys() if isinstance(node, dict) else range(len(node))

        for key in list(keys):
            value = node[key]

            if isinstance(node, dict):
                node[prefix + key] = node[key]
                value = node[prefix + key]
                del node[key]


            if isinstance(value, list) or isinstance(value, dict):
                format_value(value, prefix)


        return node
        
    stack = yaml.safe_load(stack["TemplateBody"])
    resources = stack["Resources"]

    if len(response["StackResourceDrifts"]) == 0:
        logger.warn("No drift found...\n")
        return 

    def parse(value):
        try:
            return json.loads(value)
        except:
            return value
    for resource in response["StackResourceDrifts"]:
        resource_id = resource["LogicalResourceId"]
        for diff in resource["PropertyDifferences"]:

            if diff["DifferenceType"] == "ADD":
                path = "/" + resource_id + "/Properties" + diff["PropertyPath"]
                transformed = format_value(parse(diff["ActualValue"]), "$GREEN$")
                resources = set_value_by_path(path, resources, transformed)
                
    print(apply_colors(yaml.safe_dump(resources)))



def drift(config_path, root_path):
    config = Config.parse(config_path)
    config.setup_env(Context.get_args().env)
    services = config.stacks   

    for service in services:
        if not re.search(Context.get_args().service, service.name):
            continue


        detect_drift(service.name, config)