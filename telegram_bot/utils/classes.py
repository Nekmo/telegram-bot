

def set_locals(self_target, locals_elems, to_remove=('self',)):
    for key, value in locals_elems.items():
        if key in to_remove:
            continue
        setattr(self_target, key, value)
