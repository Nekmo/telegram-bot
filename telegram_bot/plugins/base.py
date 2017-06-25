from telegram_bot.types.keyboard import register_button_function
from telegram_bot.utils.registering import RegisteringMeta, method


class Registering(RegisteringMeta):

    def validate_method(cls, name, attr):
        return getattr(attr, 'is_button_target', False)


class PluginBase(metaclass=Registering):
    def __init__(self, main):
        self.main = main
        self.db = main.db
        self.bot = main.bot
        self.register_button_targets()

    def set_handlers(self):
        pass

    def register_button_targets(self):
        for name in sorted(self.methods_by_name):
            register_button_function(getattr(self, name))


def button_target(fn):
    fn.is_button_target = True
    return fn