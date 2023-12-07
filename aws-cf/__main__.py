import argparse
from .deploy import deploy
from .utils.logging import logger

parser = argparse.ArgumentParser()

parser.add_argument("action", choices=['diff', 'deploy', 'package', "version"], help='what action to preform')
parser.add_argument("path", help='path to the file describing the services')
parser.add_argument("-v", '--version', action='version', help='path to the file describing the services', version='%(prog)s 0.0.0')
parser.add_argument("-r", "--root")

args = parser.parse_args()

if args.action:
    print("Version: ")

if args.action == "deploy":
    try:
        deploy(args.path, args.root or "")
    except Exception as e:
        logger.error(str(e))


