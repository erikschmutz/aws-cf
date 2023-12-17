from ..utils.logging import logger
from ..utils.config import Config
from ..utils.context import Context

def info():
    config = Config.parse(Context.get_service_path())
    
    envs = '\n'.join(["  🌳 " + env.name + " (" + env.region + ")"  for env in config.Environments])
    stacks = '\n'.join([f"  📚 {stack.name} ({len(stack.resources.keys())} resource)" for stack in config.Stacks])
    root_path = Context.get_root()
    service_path = Context.get_service_path()

    logger.warn(f"""

Meta:
  🛎️  services: {service_path}
  🪵  root directory: {root_path}

Environments: 
{envs} 

Stacks:
{stacks}
    """)