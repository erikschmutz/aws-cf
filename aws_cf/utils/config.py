from typing import List
from pydantic import BaseModel
import yaml
import os
from .context import Context

class Stack(BaseModel):
    path: str
    name: str

    @property
    def _path(self):
        return self.path.replace("$root", Context.get_root())
        
    @property
    def _yml(self):
        return yaml.safe_load(open(self._path).read())

    @property
    def resources(self):
        return self._yml.get("Resources", {})

class Enviroment(BaseModel):
    name: str
    profile: str
    region: str
    artifacts: str



class Config(BaseModel):
    Enviroments: List[Enviroment]
    Stacks: List[Stack]

    @staticmethod
    def parse(path: str = None):
        try:
            data = yaml.safe_load(open(path))
            return Config(**data)
        except:
            raise IOError("Not able to find file at path: " + '"' + path + '"')

    def setup_env(self, env=None):
        if not env:
            os.environ["AWS_PROFILE"] = self.Enviroments[0].profile
            os.environ["AWS_DEFAULT_REGION"] = self.Enviroments[0].region
