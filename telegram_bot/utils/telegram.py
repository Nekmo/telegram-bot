import time


IGNORE_MESSAGES_OFFTIME = 60


def get_name(name_data):
    return ' '.join(filter(lambda x: x, [name_data.first_name, name_data.last_name]))


def securize_message(fn):
    def wrapper(message, *args, **kwargs):
        if time.time() - message.date > IGNORE_MESSAGES_OFFTIME:
            return
        return fn(message, *args, **kwargs)
    return wrapper


def is_admin(bot, message):
    admins = bot.get_chat_administrators(message.chat.id)
    from_id = message.from_user.id
    for admin in admins:
        if admin.user.id == from_id:
            return True
    return False
