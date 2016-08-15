

class RegisteringMeta(type):
    def __init__(cls, name, bases, attrs):
        cls.register_init()
        for base in bases:
            cls.methods.union(base.methods)
            cls.methods_by_name.update(base.methods_by_name)
        for name, attr in attrs.items():
            if not cls.validate_method(name, attr):
                continue
            cls.register(name, attr)
        super().__init__(name, bases, attrs)

    def validate_method(cls, name, attr):
        return getattr(attr, '__name__', None) == 'api_method'

    def register(cls, name, attr):
        cls.methods.add(attr)
        cls.methods_by_name[name] = attr

    def register_init(cls):
        cls.methods = set()
        cls.methods_by_name = {}


class RegisteringBase(metaclass=RegisteringMeta):
    pass


# @method
def method(func):
    def api_method(name):
        return func(name)
    return api_method
