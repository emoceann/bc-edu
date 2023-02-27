from fastapi import FastAPI
import app.telegram.api as telegram_app
import app.dictionary.utm.api as dict_utm_app
import app.integration.nowpayments.api as nowpayments_app

app = FastAPI()
app.include_router(prefix="/telegram", router=telegram_app.app)
app.include_router(prefix="/utm", router=dict_utm_app.app)
app.include_router(prefix="/payment", router=nowpayments_app.app)
