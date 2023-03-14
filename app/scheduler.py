from rocketry import Rocketry
from core.logger import logger as log
from app.integration.bizon365 import services

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
