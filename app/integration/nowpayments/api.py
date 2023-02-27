from app.integration.nowpayments.deps import app
from app.integration.nowpayments import models
from app.integration.nowpayments.services import callback_check


@app.post('/info')
async def payment_callback(info: models.PaymentModel):
    await callback_check(info)
