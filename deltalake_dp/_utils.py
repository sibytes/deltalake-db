import yaml
from typing import Iterator
from enum import Enum

class ObjectType(Enum):
    DATABASES = 1
    TABLES = 2
    VIEWS = 3

class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True

    INDENT = 4


class Index:

    _SEP = "!"

    @classmethod
    def to_path(cls, index: str):
        return index.replace(cls._SEP, "/")

    @classmethod
    def get_index_env(cls, index: str):
        return index.split(cls._SEP)[1]

    @classmethod
    def get_index_db(cls, index: str):
        return index.split(cls._SEP)[0]

    @classmethod
    def get_index_table(cls, index: str):
        return index.split(cls._SEP)[2]

    @classmethod
    def get_index(cls, i: Iterator):
        return cls._SEP.join(i)


