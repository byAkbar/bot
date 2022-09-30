from settings.message import MESSAGES

from settings import config
from settings import utility


from handlers.handler import Handler
from data_base.dbalchemy import DBManager


class HandlerAllText(Handler):

    def __init__(self, bot):
        super().__init__(bot)
        self.step = 0

        self.BD = DBManager()


    def pressed_btn_category(self, message):

        self.bot.send_message(message.chat.id, "Каталог категории товара",
                                reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Сделай свой выбор",
                                reply_markup=self.keybords.category_menu())


    def pressed_btn_info(self, message):

        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                                parse_mode="HTML",
                                reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):

        self.bot.send_message(message.chat.id, MESSAGES["settings"],
                                parse_mode="HTML",
                                reply_markup=self.keybords.settings_menu())
    


    def pressed_btn_back(self, message):
        
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                                reply_markup=self.keybords.start_menu())


    def pressed_btn_product(self, message, product):
        self.bot.send_message(message.chat.id, 'Категория ' + config.KEYBOARD[product],
                                reply_markup=self.keybords.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок", 
                                reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):

        self.step = 0

        count = self.BD.select_all_product_id()

        quantity = self.BD.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)


    def send_message_order(self, product_id, quantity, message,):

        self.bot.send_message(message.chat.id, MESSAGES['order_number'].format(
            self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                                MESSAGES['order'].
                                format(self.BD.select_single_product_name(
                                    product_id),
                                        self.BD.select_single_product_title(
                                            product_id),
                                        self.BD.select_single_product_price(
                                            product_id),
                                        self.BD.select_order_quantity(
                                            product_id)),
                                parse_mode="HTML",
                                reply_markup=self.keybords.orders_menu(
                                    self.step, quantity))

    def pressed_btn_up(self, message):

        count = self.BD.select_all_product_id()

        quantity_order = self.BD.select_order_quantity(count[self.step])

        quantity_product = self.BD.select_single_product_quantity(count[self.step])

        if quantity_product > 0:
            quantity_order +=1
            quantity_product -=1

            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)

            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)

        self.send_message_order(count[self.step], quantity_order, message)


    def pressed_btn_douwn(self, message):

        count = self.BD.select_all_product_id()

        quantity_order = self.BD.select_order_quantity(count[self.step])

        quantity_product = self.BD.select_single_product_quantity(count[self.step])

        if quantity_order > 0:
            quantity_order -=1
            quantity_product +=1

            self.BD.update_order_value(count[self.step], 'quantity', quantity_order)

            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)

        self.send_message_order(count[self.step], quantity_order, message) 


    def pressed_btn_x(self, message):

        count = self.BD.select_all_product_id()

        if count.__len__() > 0:

            quantity_order = self.BD.select_order_quantity(count[self.step])
            
            quantity_product = self.BD.select_single_product_quantity(count[self.step])
            quantity_product += quantity_order

            self.BD.delete_order(count[self.step])

            self.BD.update_product_value(count[self.step], 'quantity', quantity_product)

            self.step -= 1

        count = self.BD.select_all_product_id()

        if count.__len__() > 0:
            
            quantity_order = self.BD.select_order_quantity(count[self.step])

            self.send_message_order(count[self.step], quantity_order, message)

        else:

            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                parse_mode="HTML",

                                reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):

        if self.step > 0:
            self.step -=1

        count = self.BD.select_all_product_id()

        quantity = self.BD.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)


    def pressed_btn_next_step(self, message):

        if self.step < self.BD.count_rows_order()-1:
            self.step +=1

        count = self.BD.select_all_product_id()

        quantity = self.BD.select_order_quantity(count[self.step])

        self.send_message_order(count[self.step], quantity, message)


    def pressed_btn_applay(self, message):

        self.bot.send_message(message.chat.id,
                                MESSAGES['applay'].format(
                                    utility.get_total_coas(self.BD),

                                    utility.get_total_quantity(self.BD)),
                                parse_mode="HTML",
                                reply_markup=self.keybords.category_menu())

        self.BD.delete_all_order()


    def handle(self):

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):

            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.pressed_btn_category(message)

            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            if message.text == config.KEYBOARD['ORDER']:

                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                            MESSAGES['no_orders'],
                                            parse_mode="HTML",
                                            reply_markup=self.keybords.
                                            category_menu())

            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')



            if message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            if message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_douwn(message)
            
            if message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            if message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            if message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_applay(message)

            else:
                self.bot.send_message(message.chat.id, message.text)