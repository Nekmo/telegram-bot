

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def remove_from_dict(d, removes, new_dict=False):
    if new_dict:
        d = dict(d)
    for to_remove in removes:
        if to_remove in d:
            del d[to_remove]
    return d


def map_dict(d, fn):
    return {k: fn(v) for k, v in d.items()}