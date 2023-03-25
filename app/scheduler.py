from rocketry import Rocketry, conds
from rocketry.log import MinimalRecord
from redbird.repos import CSVFileRepo
from pathlib import Path
from core.logger import logger as log
from app.integration.bizon365 import services
from app.telegram import services as tg_services
from app.integration.google.sheet import services as google_services
from app.integration.google.sheet.deps import g_sheet
from core.contrib.notion.services.utils import get_user_comments


app = Rocketry(
    execution="async",
    logger_repo=CSVFileRepo(filename=Path('logs/rocketry_logs.csv'), model=MinimalRecord)
)


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


@app.task(conds.daily.at('8:59') | conds.daily.at('11:59') | conds.daily.at('15:59'))
async def notify_webinar():
    await tg_services.webinar_start_notify()


@app.task('every 24 hours')
async def upload_stats_to_google():
    await google_services.statistic_upload_to_userbase_sheet(g_sheet)
    await google_services.statistic_upload_to_traffic_sheet(g_sheet)
    await google_services.statistic_upload_to_dashboard_sheet(g_sheet)


@app.task('every 1 hour')
async def comments_parse_reward():
    await get_user_comments()