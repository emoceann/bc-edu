from .deps import g_sheet
from gspread.cell import Cell
from app.statistics.services import StatisticModelBuilder


async def statistic_upload_to_sheet(sheet: g_sheet):
    dashboard_sheet = sheet.get_worksheet(0)
    build_stat = StatisticModelBuilder()
    stats = await build_stat.build()
    cells = [
        Cell(row=3, col=2, value=str(stats.count_user_bot)),
        Cell(row=4, col=2, value=str(stats.count_webinar_user)),
        # Cell(row=6, col=2, value=str(stats.count_nowpayments_all)),
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
        # Cell(row=49, col=2, value=str(stats.count_nowpayments_all))
    ]
    dashboard_sheet.update_cells(cells)

