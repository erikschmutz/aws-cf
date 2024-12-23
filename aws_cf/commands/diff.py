from ..utils.logging import logger
from ..utils.config import Config
from ..utils.context import Context
import sys
from ..utils.common import create_change_set,package, remove_change_set, format_diff,format_diffs
import re
import json 
import boto3
import hashlib

def check_cache(service, config: Config):
    str = package(service, config)
    hash = hashlib.sha256(str.encode('utf-8')).hexdigest()
    bucket, *keys = config.enviroment.cache.replace("s3://", "").split("/")
    key = "/".join(keys)
    s3 = boto3.resource("s3")

    if not key.endswith("/"):
        key += "/"

    key = key + service.path + ".lock"
    try:
        o = s3.Object(bucket, key).load()
        print(key, o)

    except Exception as e:
        if e.response['Error']['Code'] == "404":
            return False
        raise e

    print(hash)
    
def update_cache(service, config: Config):
    str = package(service, config)
    hash = hashlib.sha256(str.encode('utf-8')).hexdigest()
    bucket, *keys = config.enviroment.cache.replace("s3://", "").split("/")
    key = "/".join(keys)
    s3 = boto3.resource("s3")

    if not key.endswith("/"):
        key += "/"

    key = key + service.path + ".lock"
    try:
        o = s3.Object(bucket, key).load()
        print(key, o)

    except Exception as e:
        if e.response['Error']['Code'] == "404":
            return False
        raise e

    print(hash)

def diff(config_path, root_path):
    config = Config.parse(config_path)
    config.setup_env(Context.get_args().env)
    services = config.stacks   

    for service in services:
        if not re.search(Context.get_args().service, service.name):
            continue

        if config.enviroment.cache:
            if check_cache(service, config):
                continue

        change_set = create_change_set(service, config)
        logger.info("Created change set...")

        if change_set:
            result = format_diffs(service.name, change_set)
            logger.warn(result)
            remove_change_set(service.name, change_set["ChangeSetName"])
        
        else:
            yml = package(service, config)
            logger.warn(f"{service.name} new stack ⭐")
            logger.warn(yml)