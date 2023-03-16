from .deps import g_sheet
from gspread.cell import Cell
from app.statistics.services import StatisticModelBuilder
from app.account import services as account_services


async def statistic_upload_to_dashboard_sheet(sheet: g_sheet):
    dashboard_sheet = sheet.get_worksheet(0)
    build_stat = StatisticModelBuilder()
    stats = await build_stat.build()
    cells = [
        Cell(row=3, col=2, value=str(stats.count_user_bot)),
        Cell(row=4, col=2, value=str(stats.count_webinar_user)),
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
        Cell(row=49, col=2, value=str(stats.count_nowpayments_all))
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




