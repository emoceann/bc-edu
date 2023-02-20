from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from core.settings import settings
from app.dictionary.utm import models, dao

app = APIRouter(tags=['Api UTM'])


@app.post('/new_traffic_source')
async def new_source(traffic: models.NewTrafficSource):
    return await dao.UtmLabelDict.create(source=traffic.source, medium=traffic.medium,
                                         campaign=traffic.campaign, content=traffic.content)


@app.get('/link')
async def new_user(params: models.NewTrafficSource = Depends()):
    id_link = await dao.UtmLabelDict.get_or_none(source=params.source, medium=params.medium,
                                                 campaign=params.campaign, content=params.content)
    if id_link:
        return RedirectResponse(f'https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={id_link.id}')
    return
