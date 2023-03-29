import httpx
from app.telegram.deps import bot
from app.integration.nowpayments import models, dao
from core.settings import settings
from core.logger import logger as log
from app.telegram import deps as tg_deps


currencies = {1: 'btc', 2: 'usdttrc20'}

async def create_payment(user_id: int, invoice_id: int, coin: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            headers={
                'x-api-key': settings.NOWPAYMENT_TOKEN,
                'Content-Type': 'application/json',
            },
            url=settings.NOWPAYMENT_URL+'/invoice-payment',
            json={
                "iid": invoice_id,
                "pay_currency": currencies.get(int(coin)),
            })
        assert response.status_code == 201, f"Ошибка NowPayments, {response.status_code}"
        wallet = response.json()['pay_address']
        log.debug(f'Юзеру - {user_id} был выдан этот кошелек {wallet}, для оплаты {invoice_id}')
        return wallet


async def create_invoice(price: int, user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            headers={
                'x-api-key': settings.NOWPAYMENT_TOKEN,
                'Content-Type': 'application/json',
            },
            url=settings.NOWPAYMENT_URL + '/invoice',
            json={
                "price_amount": price,
                "price_currency": "usd",
                "order_description": user_id,
                "ipn_callback_url": settings.NOWPAYMENT_CALLBACK_URL
            })
    assert response.status_code == 200, f"Ошибка NowPayments, {response.status_code}"
    resp = response.json()
    return resp['invoice_url'], resp['id']


async def callback_check(info: models.NowPaymentInvoiceModel):
    if info.payment_status == "finished":
        await dao.NowPayment.update_or_create(**info.dict())
        await bot.send_message(settings.TELEGRAM_ADMIN_CHAT_ID, text=info.json())
        await bot.send_message(info.user_id, 'Ваша подписка оформлена')
        await tg_deps.storage.set_state(chat=info.user_id, user=info.user_id, state=None)
    elif info.payment_status == "waiting":
        await dao.NowPayment.update_or_create(**info.dict())
        await bot.send_message(settings.TELEGRAM_ADMIN_CHAT_ID, text=info.json())
        await bot.send_message(info.user_id, 'Ждем оплату')


async def nowpayments_count() -> int:
    return await dao.NowPayment.all().count()
