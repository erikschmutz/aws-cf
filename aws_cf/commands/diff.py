from ..utils.logging import logger
from ..utils.config import Config
from ..utils.context import Context
import sys
from ..utils.common import create_change_set,package, remove_change_set, format_diff
import re

def diff(config_path, root_path):
    config = Config.parse(config_path)
    config.setup_env(Context.get_args().env)
    services = config.stacks   

    for service in services:
        if not re.search(Context.get_args().service, service.name):
            continue

        change_set = create_change_set(service, config)


        if change_set:
            diffs = [format_diff(change)for change in change_set["Changes"]]
            logger.warn(f"{service.name} (changes {len(diffs)})")

            if len(diffs):
                logger.warning(f"  🆕  Found {len(diffs)} differences for the stack {service.name}")
                for diff in diffs:
                    logger.warning(f"> {diff}")
            else:
                logger.info(f"  No changes")

            remove_change_set(service.name, change_set["ChangeSetName"])
        
        else:
            yml = package(service, config)
            logger.warn(f"{service.name} new stack ⭐")
            logger.warn(yml)