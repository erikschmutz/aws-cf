from ..utils.logging import logger
from ..utils.config import Config
import sys
from ..utils.common import create_change_set, get_yml, remove_change_set, format_diff


def diff(config_path, root_path):
    config = Config.parse(config_path)
    config.setup_env()

    services = config.Stacks    

    for service in services:
        change_set = create_change_set(service.name, service.path, root_path, config)

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
            yml = get_yml(service.path, config, root_path)
            logger.warn(f"{service.name} new stack ⭐")
            logger.warn(yml)