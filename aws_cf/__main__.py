import argparse
from .deploy import deploy
from .diff import diff
from .utils.logging import logger


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("action", choices=['diff', 'deploy', 'package', "version"], help='what action to preform')
    parser.add_argument("path", help='path to the file describing the services')
    parser.add_argument("-v", '--version', action='version', help='path to the file describing the services', version='aws-cf: 0.0.0')
    parser.add_argument("-r", "--root")
    
    args = parser.parse_args()
    
    try:
        if args.action == "deploy":
            deploy(args.path, args.root or "")
        if args.action == "diff":
            diff(args.path, args.root or "")
    except Exception as e:
        logger.error(str(e))
    
    
    