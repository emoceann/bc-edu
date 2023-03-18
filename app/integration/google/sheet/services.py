from .deps import g_sheet
from gspread.cell import Cell
from app.statistics.services import StatisticModelBuilder
from app.account import services as account_services
from app.dictionary.utm import services as utmlabel_services


async def statistic_upload_to_dashboard_sheet(sheet: g_sheet):
    dashboard_sheet = sheet.get_worksheet(0)
    build_stat = StatisticModelBuilder()
    stats = await build_stat.build()
    cells = [
        Cell(row=3, col=2, value=str(stats.count_user_bot)),
        Cell(row=4, col=2, value=str(stats.count_webinar_user)),
        Cell(row=5, col=2, value=str(0)),
        Cell(row=6, col=2, value=str(stats.count_nowpayments_all)),
        Cell(row=8, col=2, value=str(stats.count_traffic_all)),
        Cell(row=9, col=2, value=str(stats.count_traffic_target)),
        Cell(row=11, col=2, value=str(stats.count_traffic_telegram)),

        Cell(row=14, col=2, value=str(stats.count_webinar_user)),
        Cell(row=15, col=2, value=str(stats.count_webinar_users_by_1_hour)),
        Cell(row=16, col=2, value=str(stats.count_webinar_users_by_2_hour)),
        Cell(row=17, col=2, value=str(stats.count_webinar_users_by_3_hour)),
        Cell(row=18, col=2, value=str(stats.count_webinar_users_ban)),

        Cell(row=28, col=2, value=str(stats.count_user_bot)),
        Cell(row=29, col=2, value=str(stats.count_users_expert)),
        Cell(row=30, col=2, value=str(stats.count_users_newbie)),
        Cell(row=36, col=2, value=str(stats.count_newbie_test_finished)),
        Cell(row=37, col=2, value=str(stats.count_users_test_above_six)),
        Cell(row=38, col=2, value=str(stats.count_newbie_knowledge_base_red)),
        Cell(row=49, col=2, value=str(stats.count_nowpayments_all)),

        Cell(row=19, col=2, value=str(0)),  # Метрики которых нет
        Cell(row=21, col=2, value=str(0)),
        Cell(row=22, col=2, value=str(0)),
        Cell(row=23, col=2, value=str(0)),
        Cell(row=24, col=2, value=str(0)),
        Cell(row=25, col=2, value=str(0)),
        Cell(row=31, col=2, value=str(0)),
        Cell(row=32, col=2, value=str(0)),
        Cell(row=33, col=2, value=str(0)),
        Cell(row=40, col=2, value=str(0)),
        Cell(row=41, col=2, value=str(0)),
        Cell(row=42, col=2, value=str(0)),
        Cell(row=43, col=2, value=str(0)),
        Cell(row=45, col=2, value=str(0)),
        Cell(row=46, col=2, value=str(0)),
        Cell(row=47, col=2, value=str(0)),
        Cell(row=49, col=2, value=str(0)),
        Cell(row=50, col=2, value=str(0)),
        Cell(row=51, col=2, value=str(0)),
        Cell(row=52, col=2, value=str(0)),
        Cell(row=55, col=2, value=str(0)),
        Cell(row=56, col=2, value=str(0)),
        Cell(row=57, col=2, value=str(0)),
        Cell(row=58, col=2, value=str(0)),
        Cell(row=59, col=2, value=str(0))
    ]
    dashboard_sheet.update_cells(cells)


async def statistic_upload_to_userbase_sheet(sheet: g_sheet):
    cells = []
    userbase_sheet = sheet.get_worksheet(3)
    users = await account_services.get_all_users()
    row_start = 2
    for i in users:
        user_cells = [
            Cell(row=row_start, col=1, value=i.full_name),
            Cell(row=row_start, col=2, value=i.username),
            Cell(row=row_start, col=3, value=i.email),
            Cell(row=row_start, col=4, value=i.phone_number),
            Cell(row=row_start, col=5, value=i.is_admin)
        ]
        cells += user_cells
        row_start += 1
    userbase_sheet.update_cells(cells)


async def statistic_upload_to_traffic_sheet(sheet: g_sheet):
    cells = []
    traffic_sheet = sheet.get_worksheet(1)
    utm_labels = await utmlabel_services.get_utm_label_all()
    start_row = 3
    for count, value in enumerate(utm_labels):
        utm_label_cells = [
            Cell(row=start_row, col=1, value=count),
            Cell(
                row=start_row, col=2, value=str(
                    f'utm_source={value.source}&=utm_medium={value.medium}&utm_campaign{value.campaign}&_utmcontent{value.content}')),
            Cell(row=start_row, col=3, value=await utmlabel_services.get_count_users_by_utm_label(value.id)),
            Cell(row=start_row, col=4, value=await utmlabel_services.get_count_webinar_users_by_utmlabel(value.id))
        ]
        start_row += 1
        cells += utm_label_cells
    traffic_sheet.update_cells(cells)
