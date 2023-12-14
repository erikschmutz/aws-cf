from ..utils.logging import logger
from ..utils.common import get_yes_or_no
import os 
import shutil

def init():
    logger.warn("Creating new aws-cf project")
    name = input("Enter name (default ./)")
    path = name or "./"
    create_aws_folder = get_yes_or_no("Do you want to create a aws folder in the project?")
    

    if os.path.exists(path) and len(os.listdir(f"{path}")) != 0:
        raise Exception("Init project needs to be in an empty directory")

    if create_aws_folder:
        source = os.path.dirname(os.path.realpath(__file__)) + "/../assets/default"
    else:
        source = os.path.dirname(os.path.realpath(__file__)) + "/../assets/simple"
        shutil.copytree(source, path + "/")
        