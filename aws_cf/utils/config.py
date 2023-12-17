from typing import List, Optional
from pydantic import BaseModel
import yaml
import os
from .context import Context

class Stack(BaseModel):
    path: str
    name: str
    envs: Optional[List[str]] = None
    parameters: Optional[dict] = None

    @property
    def _path(self):
        return self.path.replace("$root", Context.get_root())
        
    @property
    def _yml(self):
        class SafeLoaderIgnoreUnknown(yaml.SafeLoader):
            def ignore_unknown(self, node):
                return None 

        SafeLoaderIgnoreUnknown.add_constructor(None, SafeLoaderIgnoreUnknown.ignore_unknown)

        return yaml.load(open(self._path).read(), Loader=SafeLoaderIgnoreUnknown)

    @property
    def resources(self):
        return self._yml.get("Resources", {})

class Enviroment(BaseModel):
    artifacts: str 
    name: str
    region: Optional[str] = None
    profile: Optional[str] = None



class Config(BaseModel):
    Stacks: List[Stack]
    Environments: List[Enviroment]

    @property
    def stacks(self):
        if not Context.args.env:
            return self.Stacks

        return [stack for stack in self.Stacks if not stack.envs or Context.args.env in stack.envs]

    @staticmethod
    def parse(path: str = None):
        try:
            data = yaml.safe_load(open(path))
        except:
            raise IOError("Not able to find file at path: " + '"' + path + '"')
        try:
            return Config(**data)
        except Exception as e:
            raise Exception("Not able to pase config: " + '"' + str(e) + '"')

    def setup_env(self, env=None):
        _env = self.enviroment
        
        os.environ["AWS_PROFILE"] = _env.profile
        os.environ["AWS_DEFAULT_REGION"] = _env.region

    @property
    def enviroment(self):
        env = Context.args.env
        _env = None

        if env:
            for e in self.Environments:
                if e.name == env:
                    _env = e
                    break

        else:
            _env =  self.Environments[0]
        
        if not _env and env:
            raise Exception("Not able to find env with name " + env)
        
        if not _env:
            raise Exception("Not able to find env")

        return _env
