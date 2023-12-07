from typing import List
from pydantic import BaseModel
import yaml

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