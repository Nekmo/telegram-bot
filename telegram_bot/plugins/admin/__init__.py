from telegram_bot.plugins.base import PluginBase, button_target


class AdminPlugin(PluginBase):
    def set_handlers(self):
        self.main.set_message_handler(self.test, commands=['test'])

    def test(self, message):
        msg = message.response('Una pregunta')
        inline = msg.inline_keyboard()
        inline.add_button('Opción 1', callback=self.test2)
        inline.add_button('Opción 2', json_data='2')
        msg.send()

    @button_target
    def test2(self):
        print('test2')
