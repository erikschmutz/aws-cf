import sys
from ..utils.config import Config
from ..utils.common import package

if __name__ == "__main__":
    config_path = sys.argv[1]
    root_path = sys.argv[2]
    stack_name = sys.argv[3]

    config = Config.parse(config_path)
    stack = config.Stacks[0]
    yml = open(stack.path.replace("$root", root_path).read())

    package(stack, config)
