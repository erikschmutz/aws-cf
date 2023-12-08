import argparse
from .commands.deploy import deploy
from .commands.diff import diff
from .commands.info import info
from .utils.logging import logger
from .utils.context import Context

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "action", 
        choices=['diff', 'info', 'deploy', 'package', "version"], 
        help='what action to preform'
    )

    parser.add_argument(
        "-path", "--path",
        default="services.yml",
        help='path to the file describing the services'
    )
    parser.add_argument("-v", '--version', action='version', help='path to the file describing the services', version='aws-cf: 0.0.0')
    parser.add_argument("-r", "--root")

    args = parser.parse_args()

    try:
        Context.set_root(args.root or ".")
        Context.set_service_path(args.path)

        if args.action == "deploy":
            deploy(args.path, args.root or ".")

        if args.action == "info":
            info()

        if args.action == "diff":
            diff(args.path, args.root or ".")

    except Exception as e:
        logger.error(str(e))



if __name__ == '__main__':
    main()