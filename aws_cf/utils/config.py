from typing import List
from pydantic import BaseModel
import yaml
import os

class Stack(BaseModel):
    path: str
    name: str

class Enviroment(BaseModel):
    name: str
    profile: str
    region: str
    artifacts: str

class Config(BaseModel):
    Enviroments: List[Enviroment]
    Stacks: List[Stack]

    @staticmethod
    def parse(path: str):
        try:
            data = yaml.safe_load(open(path))
            return Config(**data)
        except:
            raise IOError("Not able to find file at path: " + '"' + path + '"')

    def setup_env(self, env=None):
        if not env:
            os.environ["AWS_PROFILE"] = self.Enviroments[0].profile
            os.environ["AWS_DEFAULT_REGION"] = self.Enviroments[0].region