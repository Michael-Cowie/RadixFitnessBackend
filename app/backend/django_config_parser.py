from configparser import RawConfigParser
from os import getenv
from os.path import dirname, join


class DjangoConfigParser(RawConfigParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read(join(dirname(__file__), "defaults.ini"))

    def __getitem__(self, item):
        raise NotImplemented("Use .get() to retrieve data instead of indexing")

    def get(self, section, option, *, raw=False, vars=None):
        if env := getenv(option):
            return env
        return super().get(section, option, raw=raw, vars=vars)


django_configs = DjangoConfigParser()
