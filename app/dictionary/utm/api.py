from .deps import app
from .services import *
from fastapi import Depends
from core.settings import settings
from fastapi.responses import RedirectResponse


@app.get("/link")
async def register_user(rq: UtmLabelRq = Depends()):
    if utm := await get_utm_by(model=rq):
        return RedirectResponse(url=settings.TELEGRAM_BOT_LINK + "?start=" + str(utm.id))
    return RedirectResponse(settings.TELEGRAM_BOT_LINK)
