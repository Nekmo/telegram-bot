import json

from telebot.types import InlineKeyboardButton as TelebotInlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup

from telegram_bot.crypt import encrypt


last_module = None
last_button = 0
button_targets = {}
button_targets_keys = {}


def register_button_function(fn):
    global last_button, button_targets, last_module
    if last_module and fn.__module__ != last_module:
        last_button += 100
    if fn.__module__ != last_module:
        last_module = fn.__module__
    last_button += 1
    button_targets[last_button] = fn
    button_targets_keys[fn] = last_button
    return fn


def get_button_function_key(fn):
    return button_targets_keys[fn]


def get_button_function(id):
    return button_targets[id]


class InlineKeyboardButton(TelebotInlineKeyboardButton):
    def __init__(self, main, text, url=None, callback_data=None, switch_inline_query=None, json_data=None,
                 callback=None, callback_kwargs=None):
        self.main = main
        callback_data = callback_data or self.generate_data(json_data) or self.generate_callback(callback,
                                                                                                 callback_kwargs)
        super(InlineKeyboardButton, self).__init__(text, url=url, callback_data=callback_data,
                                                   switch_inline_query=switch_inline_query)

    def generate_data(self, data):
        if data is None:
            return
        key = self.main.config['api_token'].split(':')[1][:16].encode('utf-8')
        data = json.dumps(data)
        encoded = encrypt(data, key)
        return encoded

    def generate_callback(self, fn, callback_kwargs):
        if fn is None:
            return
        return self.generate_data({'fn': get_button_function_key(fn), 'kw': callback_kwargs})


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, main, row_width=3):
        self.main = main
        super(InlineKeyboard, self).__init__(row_width=row_width)

    def add_button(self, text, url=None, callback_data=None, switch_inline_query=None, json_data=None,
                   callback=None, callback_kwargs=None):
        self.add(InlineKeyboardButton(self.main, text, url=url, callback_data=callback_data,
                                      switch_inline_query=switch_inline_query, json_data=json_data, callback=callback,
                                      callback_kwargs=callback_kwargs))


class ReplyKeyboard(ReplyKeyboardMarkup):
    def add_button(self, text, request_contact=None, request_location=None):
        self.add(KeyboardButton(text, request_contact, request_location))
