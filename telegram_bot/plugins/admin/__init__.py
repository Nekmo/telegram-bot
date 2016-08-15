import html

import re

from telegram_bot.plugins.base import PluginBase, button_target
from telegram_bot.utils.dicts import map_dict
from telegram_bot.utils.telegram import get_name, escape_items


class AdminPlugin(PluginBase):
    def set_handlers(self):
        self.main.set_message_handler(self.test, commands=['test'])
        self.main.set_message_handler(self.ban, commands=['ban'])

    def ban(self, message):
        if not message.reply_to_message:
            return message.send_response('Responde a un mensaje para poder usar este comando.')
        moderator = message.from_user
        banned = message.reply_to_message.from_user
        # self.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        msg = message.response('<code>{b} ({bi})</code> banned by <code>{m} ({mi})</code>'.format(
            **escape_items(b=get_name(banned), bi=banned.id, m=get_name(moderator), mi=moderator.id)),
            parse_mode='html')
        inline = msg.inline_keyboard()
        inline.add_button('Unban', callback=self.unban_button, callback_kwargs={'u': banned.id})
        msg.send()

    @button_target
    def unban_button(self, query, u):
        moderator = query.from_user
        unbanned = query.message.from_user
        unbanned_name = re.findall('([^\(]+)', query.message.text)
        unbanned_name = unbanned_name[0] if unbanned_name else '??'
        self.bot.answer_callback_query(query.id, 'User unbaned')
        self.bot.edit_message_text('<code>{u} ({ui})</code> unbanned by <code>{m} ({mi})</code>'.format(
            **escape_items(u=unbanned_name, ui=unbanned.id, m=get_name(moderator), mi=moderator.id)),
            query.message.chat.id, message_id=query.message.message_id, parse_mode='html')

    def test(self, message):
        msg = message.response('Una pregunta')
        inline = msg.inline_keyboard()
        inline.add_button('Opción 1', callback=self.test2)
        inline.add_button('Opción 2', json_data='2')
        msg.send()

    @button_target
    def test2(self):
        print('test2')
