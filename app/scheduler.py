from rocketry import Rocketry
from core.logger import logger as log
from app.integration.bizon365 import services

app = Rocketry(execution="async")


@app.task('every 1 hours')
async def actual_webinar_rooms():
    """ Актуализация списка вебинарных комнат из внешнего источника """
    log.debug(f"Запущен таск актуализации списка вебинарных комнат из внешнего источника")
    await services.webinars_get_subpages()
