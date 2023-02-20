from fastapi import FastAPI
import app.telegram.api as telegram_app
import app.dictionary.api as dictionary_app

app = FastAPI()
app.include_router(prefix="/telegram", router=telegram_app.app)
app.include_router(prefix="/utm", router=dictionary_app.app)

