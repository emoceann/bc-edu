import gspread
from core.settings import settings


gc = gspread.service_account('gaccount.json')
g_sheet = gc.open_by_url(settings.GOOGLE_SHEET_URL_TOKEN)
