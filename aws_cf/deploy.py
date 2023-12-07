from .utils.logging import logger
from .utils.config import Config
import sys
import json
from .utils.common import create_change_set, remove_change_set, format_diff, get_yes_or_no, deploy_stack


def deploy(config_path, root_path):
    config = Config.parse(config_path)
    config.setup_env()
    services = config.Stacks
    logger.warning(f"Checking difference for stacks from file {config_path}")
    
    logger.info(f"* Found {len(services)} services checking differences...")

    for service in services:
        change_set = create_change_set(service.name, service.path, root_path, config)
        diffs = [format_diff(change)for change in change_set["Changes"]]

        if len(diffs):
            logger.warning(f"Found {len(diffs)} differences for the stack {service.name}")
            for diff in diffs:
                logger.warning(f"> {diff}")
            
            should_continue = get_yes_or_no(f"Do you wish to continue to update serivce: {service.name}")

            if not should_continue:
                remove_change_set(service.name, change_set["ChangeSetName"])
            else:
                logger.info("Deploying serivce...")
                deploy_stack(service.name, change_set["ChangeSetName"])
        else:
            logger.info(f"Found no differences for the stack {service.name}")

        
