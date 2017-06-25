import datetime

from telegram_bot.plugins.base import PluginBase, button_target
from telegram_bot.types.keyboard import InlineKeyboard
from telegram_bot.utils.telegram import username_id_code, get_name, escape_items


class ModeratorsPlugin(PluginBase):
    def set_handlers(self):
        self.main.set_message_handler(self.mod, commands=['mod'])

    def mod(self, message):
        moderator = message.reply_to_message.from_user
        group_id = message.chat.id
        keyboard = InlineKeyboard(self.main)
        keyboard.add_button('Remove mod', callback=self.rm_mod, callback_kwargs={'u': moderator.id})
        if self.db.moderators.find_one({'group_id': group_id, 'moderator.id': moderator.id}):
            message.send_response('{} is already moderator in this groupchat'.format(username_id_code(moderator)),
                                  parse_mode='html', reply_markup=keyboard)
        else:
            self.db.moderators.insert_one({'group_id': group_id, 'moderator': vars(moderator),
                                           'created_at': datetime.datetime.now()})
            message.send_response('Now {} is a moderator in this group'.format(username_id_code(moderator)),
                                  parse_mode='html', reply_markup=keyboard)

    @button_target
    def rm_mod(self, query, u):
        group_id = query.message.chat.id
        q = {'group_id': group_id, 'moderator.id': u}
        mod_data = self.db.moderators.find_one(**q)
        if mod_data is None:
            return self.bot.answer_callback_query(query.id, 'Not mod removed. {} is a mod?'.format(u))
        self.db.moderators.delete_many(**q)
        self.bot.answer_callback_query(query.id, 'Removed {} moderator'.format(get_name(mod_data.moderator)))
        self.bot.edit_message_text('{} is no longer a moderator in this group.'.format(
            username_id_code(mod_data.moderator)), query.message.chat.id, message_id=query.message.message_id,
            parse_mode='html')

    def mod_db(self, group_id, moderator, is_mod=True):
        self.db.moderators.find_one(group_id=group_id, )
