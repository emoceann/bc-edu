from app.telegram.deps import bot, dp
from app.telegram.handler.states import NewUser
from aiogram import types
from aiogram.dispatcher import FSMContext
from app.telegram.services import get_template
from app.integration.nowpayments import services as nowpayments_services

# @dp.message_handler(commands='payment')
# async def payment(msg: types.Message, state: FSMContext):
#     text = get_template('payments.html', content_list=dict(sub_month={}, sub_month_ids={}))
#     buttons = [i for i in zip(text['sub_month'].split('\n'), text['sub_month_ids'].split('\n'))]
#     buttons = buttons[1:len(buttons)-1]
#     markup = types.InlineKeyboardMarkup().add(*(types.InlineKeyboardButton(text=i[0], callback_data=i[1]) for i in buttons))
#     await msg.reply('Выберите тип подписки', reply_markup=markup)
#     await NewUser.order_subscription.set()


@dp.callback_query_handler(state=NewUser.order_subscription)
async def payment_coin(cb: types.CallbackQuery, state: FSMContext):
    url, invoice_id = await nowpayments_services.create_invoice(price=int(cb.data), user_id=str(cb.from_user.id))
    await state.update_data(invoice_id=invoice_id, url=url)
    markup = types.InlineKeyboardMarkup().add(
        *(types.InlineKeyboardButton(text='Оплата в боте', callback_data='1'), types.InlineKeyboardButton(text='Оплата через сайт', callback_data='2')))
    await bot.edit_message_text('Каким способом хотите совершить оплату?', chat_id=cb.from_user.id, message_id=cb.message.message_id,inline_message_id=cb.inline_message_id, reply_markup=markup)
    await NewUser.order_wait.set()

@dp.callback_query_handler(state=NewUser.order_wait)
async def payment_wallet_or_url(cb: types.CallbackQuery, state: FSMContext):
    if cb.data == '1':
        text = get_template('payments.html', content_list=dict(currency={}))
        markup = types.InlineKeyboardMarkup().add(
            *(types.InlineKeyboardButton(text=v, callback_data=str(i)) for i, v in enumerate(text['currency'].split('\n'))))
        await bot.edit_message_text(
            'Выберите тип крипты которой будете оплачивать',
            chat_id=cb.from_user.id,
            message_id=cb.message.message_id, inline_message_id=cb.inline_message_id,
            reply_markup=markup
        )
        await NewUser.order_wait_coin.set()

    if cb.data == '2':
        url = (await state.get_data())['url']
        await bot.edit_message_text(
            url,
            chat_id=cb.from_user.id,
            message_id=cb.message.message_id,
            inline_message_id=cb.inline_message_id
        )


@dp.callback_query_handler(state=NewUser.order_wait_coin)
async def payment_wallet(cb: types.CallbackQuery, state: FSMContext):
    invoice_id = (await state.get_data())['invoice_id']
    wallet = await nowpayments_services.create_payment(cb.from_user.id, invoice_id, int(cb.data))
    await bot.send_message(cb.from_user.id, f'Пожалуйста оплатите по этому адресу \n {wallet}')