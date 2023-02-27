import httpx
from app.account.dao import User
from app.telegram.deps import bot
from app.integration.nowpayments import models, dao
from core.settings import settings


url = "https://api-sandbox.nowpayments.io/v1/invoice-payment"


async def create_payment(user_id: int, invoice_id: int, coin: str):
    payload = {
        "iid": invoice_id,
        "pay_currency": coin,
        "order_description": user_id
        # "ipn_callback_url": "https://e139-213-230-80-167.eu.ngrok.io/payment/info" не доступен в сэндбоксе, но есть в офиц апи
    }
    headers = {
        'x-api-key': settings.NOWPAYMENT_TOKEN,
        'Content-Type': 'application/json',
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(headers=headers, url=url, json=payload)
        wallet = response.json()['pay_address']
        return wallet


async def callback_check(info: models.PaymentModel):
    if info.payment_status == "finished":
        await dao.Payment.update_or_create(**info.dict())
        await bot.send_message(settings.TELEGRAM_ADMIN_CHAT_ID, text=info.json())
