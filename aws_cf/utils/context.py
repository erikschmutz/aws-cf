from typing import Any

class Context:
    root: str
    service_path: str
    args: Any

    @staticmethod
    def get_args():
        return Context.args

    @staticmethod
    def set_args(args):
        Context.args = args


    @staticmethod
    def get_changeset_prefix():
        return "AWSCF"

    @staticmethod
    def set_root(root: str):
        Context.root = root

    @staticmethod
    def get_root():
        return Context.root

    @staticmethod
    def set_service_path(path: str):
        Context.service_path = path

    @staticmethod
    def get_service_path():
        return Context.service_path