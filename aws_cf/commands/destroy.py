from ..utils.logging import logger
from ..utils.config import Config
from ..utils.context import Context
import sys
import re
import json
from ..utils.common import delete_stack, remove_change_set, format_diff, get_yes_or_no, deploy_stack, create_stack,package


def destroy(config_path, root_path):
    config = Config.parse(config_path)
    config.setup_env(Context.get_args().env)
    services = config.stacks
    
    for service in services:
        if not re.search(Context.get_args().service, service.name):
            continue

                
        logger.error(f"❗❗Warning about to delete stack {service.name}❗❗")
        should_continue = get_yes_or_no(f"Are you sure that you want to delete: {service.name}?")

        if should_continue:
            delete_stack(service.name)


        
