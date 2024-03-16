from ..utils.logging import logger
from ..utils.common import get_yes_or_no
import os 
import shutil
import requests
import zipfile


ZIP_URL = "https://github.com/erikschmutz/aws-cf/raw/main/aws_cf/assets/templates/example-template.zip"

def init():
    logger.warn("Creating new aws-cf project")
    name = input("Enter name (default ./)")
    path = name or "./"
    # create_aws_folder = get_yes_or_no("Do you want to create a aws folder in the project?")
    
    if os.path.exists(path) and len(os.listdir(f"{path}")) != 0:
        raise Exception("Init project needs to be in an empty directory")
    
    body = requests.get(ZIP_URL).content

    with open("./tmp.zip", "wb") as f:
        f.write(body)

    with zipfile.ZipFile("tmp.zip", 'r') as zip_ref:
        zip_ref.extractall(".")
     

    os.remove("tmp.zip")