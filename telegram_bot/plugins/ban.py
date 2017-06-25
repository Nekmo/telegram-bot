import html
import json

import re

import datetime

from telebot.apihelper import ApiException

from telegram_bot.plugins.base import PluginBase, button_target
from telegram_bot.utils.dicts import AttrDict
from telegram_bot.utils.telegram import get_name, escape_items


def send_error(message, e):
    error = json.loads(e.result.text)
    msg = '<b>An error has occurred!</b> {error}'.format(**escape_items(error=error['description']))
    message.send_response(msg, parse_mode='html')


class FakeUser(AttrDict):
    id = None


class BanPlugin(PluginBase):
    def set_handlers(self):
        self.main.set_message_handler(self.ban, commands=['ban'])

    def ban(self, message):
        if not message.reply_to_message:
            return message.send_response('Use this command responding to a message written by the user to ban.')
        group_id = message.chat.id
        moderator = message.from_user
        banned = message.reply_to_message.from_user
        try:
            self.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        except ApiException as e:
            return send_error(message, e)
        msg = message.response('<code>{b} ({bi})</code> banned by <code>{m} ({mi})</code>'.format(
            **escape_items(b=get_name(banned), bi=banned.id, m=get_name(moderator), mi=moderator.id)),
            parse_mode='html')
        inline = msg.inline_keyboard()
        inline.add_button('Unban', callback=self.unban_button, callback_kwargs={'u': banned.id})
        msg.send()
        self.ban_db(group_id, moderator, banned)

    def ban_db(self, group_id, moderator, banned, is_banned=True):
        bans = self.db.bans
        update_data = {'moderator': vars(moderator), 'is_banned': is_banned,
                       'banned_at' if is_banned else 'unbanned_at': datetime.datetime.now()}
        if len(vars(banned)) > 1:
            update_data['banned'] = vars(banned)
        if not bans.update_one({'group_id': group_id, 'moderator.id': moderator.id, 'banned.id': banned.id},
                               {'$set': update_data}).matched_count:
            update_data.update({'group_id': group_id, 'unbanned_at' if is_banned else 'banned_at': None,
                                'banned': vars(banned)})
            bans.insert_one(update_data)

    @button_target
    def unban_button(self, query, u):
        chat_id = query.message.chat.id
        moderator = query.from_user
        unbanned_id = u
        unbanned_name = re.findall('([^\(]+)', query.message.text)
        unbanned_name = unbanned_name[0] if unbanned_name else '??'
        self.bot.answer_callback_query(query.id, 'User unbaned')
        self.bot.edit_message_text('<code>{u} ({ui})</code> <b>un</b>banned by '
                                   '<code>{m} ({mi})</code> at <i>{dt}</i>'.format(
            **escape_items(u=unbanned_name, ui=unbanned_id, m=get_name(moderator), mi=moderator.id,
                           dt=datetime.datetime.now().strftime('%c'))),
            query.message.chat.id, message_id=query.message.message_id, parse_mode='html')
        self.bot.unban_chat_member(chat_id, unbanned_id)
        self.ban_db(chat_id, moderator, FakeUser(id=unbanned_id), False)
