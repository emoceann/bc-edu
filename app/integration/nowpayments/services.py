import httpx
from app.telegram.deps import bot
from app.integration.nowpayments import models, dao
from core.settings import settings
from core.logger import logger as log


async def create_payment(user_id: int, invoice_id: int, coin: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            headers={
                'x-api-key': settings.NOWPAYMENT_TOKEN,
                'Content-Type': 'application/json',
            },
            url=settings.NOWPAYMENT_URL,
            json={
                "iid": invoice_id,
                "pay_currency": coin,
                "order_description": user_id
                # "ipn_callback_url": settings.NOWPAYMENT_URL не доступен в сэндбоксе, но есть в офиц апи
            })
        assert response.status_code == 200, f"Ошибка NowPayments, {response.status_code}"
        wallet = response.json()['pay_address']
        log.debug(f'Юзеру - {user_id} был выдан этот кошелек {wallet}, для оплаты {invoice_id}')
        return wallet


async def callback_check(info: models.NowPaymentInvoiceModel):
    if info.payment_status == "finished":
        await dao.NowPayment.update_or_create(**info.dict())
        await bot.send_message(settings.TELEGRAM_ADMIN_CHAT_ID, text=info.json())
