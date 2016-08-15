import json


class Config(dict):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.read(self.path)

    def read(self, path):
        path = path or self.path
        self.clear()
        self.update(json.load(open(path)))
