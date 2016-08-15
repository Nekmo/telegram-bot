

def remove_from_dict(d, removes, new_dict=False):
    if new_dict:
        d = dict(d)
    for to_remove in removes:
        if to_remove in d:
            del d[to_remove]
    return d
