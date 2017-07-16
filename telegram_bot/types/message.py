import telebot.types
from telebot.types import Message as TelebotMessage, ForceReply

from telegram_bot.types.keyboard import InlineKeyboard, ReplyKeyboard
from telegram_bot.utils.classes import set_locals

class ResponseMessage(object):
    destination_key = 'chat'
    chat_id = None
    main = None
    text = None
    message = None
    disable_web_page_preview = None
    reply_to_message_id = None
    reply_markup = None
    parse_mode = None
    disable_notification = None

    def __init__(self, message, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 parse_mode=None, disable_notification=None, destination_key='chat'):
        set_locals(self, locals())
        self.main = message.main

    def set_private(self):
        self.destination_key = 'from_user'

    def set_public(self):
        self.destination_key = 'chat'

    def get_destination_id(self):
        return getattr(self.message, self.destination_key).id

    def inline_keyboard(self, row_width=3):
        self.reply_markup = InlineKeyboard(self.message.main, row_width)
        return self.reply_markup

    def _reply_function(self, function):
        def wrapper(msg):
            if msg.text.startswith('/'):
                return
            msg = Message.from_telebot_message(self.main, msg)
            function(msg)
        self.main.bot.register_next_step_handler(self.message, wrapper)

    def force_reply(self, function, selective=False):
        self._reply_function(function)
        self.reply_markup = ForceReply(selective)

    def reply_keyboard(self, function, row_width=2):
        self._reply_function(function)
        self.reply_markup = ReplyKeyboard(row_width)
        return self.reply_markup

    def send(self):
        chat_id = self.chat_id or self.get_destination_id()
        return self.main.bot.send_message(chat_id, self.text, disable_web_page_preview=self.disable_web_page_preview,
                                          reply_to_message_id=self.reply_to_message_id, reply_markup=self.reply_markup,
                                          parse_mode=self.parse_mode, disable_notification=self.disable_notification)


class Message(TelebotMessage):
    def __init__(self, main, message_id, from_user, date, chat, content_type, **options):
        self.main = main
        self.bot = main.bot
        super(Message, self).__init__(message_id, from_user, date, chat, content_type, options)

    @classmethod
    def from_telebot_message(cls, main, msg):
        return cls(main, **vars(msg))

    def response(self, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 parse_mode=None, disable_notification=None, destination_key='chat'):
        return ResponseMessage(self, text, disable_web_page_preview=disable_web_page_preview,
                               reply_to_message_id=reply_to_message_id, reply_markup=reply_markup,
                               parse_mode=parse_mode,disable_notification=disable_notification,
                               destination_key=destination_key)

    def send_response(self, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                      parse_mode=None, disable_notification=None, destination_key='chat'):
        return self.response(text, disable_web_page_preview=disable_web_page_preview,
                             reply_to_message_id=reply_to_message_id, reply_markup=reply_markup,
                             parse_mode=parse_mode, disable_notification=disable_notification,
                             destination_key=destination_key).send()

    def send_private(self, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                     parse_mode=None, disable_notification=None):
        return self.send_response(text, disable_web_page_preview=disable_web_page_preview,
                                  reply_to_message_id=reply_to_message_id, reply_markup=reply_markup,
                                  parse_mode=parse_mode, disable_notification=disable_notification,
                                  destination_key='from_user')

    def reply(self, text, disable_web_page_preview=None, reply_markup=None, parse_mode=None, disable_notification=None):
        return self.send_response(text, disable_web_page_preview=disable_web_page_preview,
                                  reply_to_message_id=self.chat.id, reply_markup=reply_markup,
                                  parse_mode=parse_mode, disable_notification=disable_notification,
                                  destination_key='chat')


def message_wrapper(main, fn):
    def wrapper(message, *args, **kwargs):
        return fn(Message.from_telebot_message(main, message), *args, **kwargs)
    return wrapper
