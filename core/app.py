from fastapi import FastAPI
import app.telegram.api as telegram_app

app = FastAPI()
app.include_router(prefix="/telegram", router=telegram_app.app)


