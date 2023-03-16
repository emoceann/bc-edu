from rocketry import Rocketry, conds
from core.logger import logger as log
from app.integration.bizon365 import services
from app.telegram import services as tg_services
from datetime import datetime

app = Rocketry(execution="async")


@app.task('every 2 hours')
async def actual_webinar_rooms():
    """ Актуализация списка вебинарных комнат из внешнего источника """
    log.debug(f"Запущен таск актуализации списка вебинарных комнат из внешнего источника")
    await services.webinars_get_subpages()


@app.task('every 3 hours')
async def webinars_refresh_reports():
    """ Получение список доступных отчетов и последующее обновление БД """
    log.debug("Запущен таск получения списка доступных отчетов и последующее обновление БД")
    await services.webinars_refresh_reports()


@app.task('every 5 hours')
async def in_process_report():
    """  """
    if webinar_id := await services.get_first_un_closed_webinar_report():
        await services.webinars_get_detail_report(webinar_id=webinar_id)


@app.task('every 24 hours')
async def notify_not_active():
    await tg_services.notify_24_hours()


@app.task('every 1 hour')
async def notify_before_webinar():
    await tg_services.webinar_before_notify()


@app.task(conds.daily.at('11:59') | conds.daily.at('14:59') | conds.daily.at('18:59'))
async def notify_webinar():
    await tg_services.webinar_start_notify()
