import html
import time

from telegram_bot.exceptions import StopException
from telegram_bot.utils.dicts import map_dict

IGNORE_MESSAGES_OFFTIME = 60


def get_name(name_data):
    return ' '.join(filter(lambda x: x, [name_data.first_name, name_data.last_name]))


def securize_message(fn):
    def wrapper(message, *args, **kwargs):
        if time.time() - message.date > IGNORE_MESSAGES_OFFTIME:
            return
        return fn(message, *args, **kwargs)
    return wrapper


def catch_errors(fn):
    def wrapper(message, *args, **kwargs):
        try:
            return fn(message, *args, **kwargs)
        except StopException:
            pass
    return wrapper


def is_admin(bot, message):
    admins = bot.get_chat_administrators(message.chat.id)
    from_id = message.from_user.id
    for admin in admins:
        if admin.user.id == from_id:
            return True
    return False


def escape_items(**d):
    return map_dict(d, lambda x: x if isinstance(x, int) else html.escape(x))


def username_id_code(user):
    return '<code>{name} ({id})</code>'.format(name=html.escape(get_name(user)), id=user.id)
