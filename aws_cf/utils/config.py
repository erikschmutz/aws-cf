from typing import List, Optional
from pydantic import BaseModel
import yaml
import os
from .context import Context

class Stack(BaseModel):
    path: str
    name: str
    parameters: Optional[dict]

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
    Enviroments: List[Enviroment]

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
        if not env:
            if self.Enviroments[0].profile:
                os.environ["AWS_PROFILE"] = self.Enviroments[0].profile

            if self.Enviroments[0].region:
                os.environ["AWS_DEFAULT_REGION"] = self.Enviroments[0].region
