from aiogram.dispatcher.filters.state import StatesGroup, State


class NewUser(StatesGroup):
    new_or_experienced = State()  # стейт новичок или продвинутый
    experienced = State()  # стейт продвинутого
    experienced_info = State()
    experienced_choose = State()
    newbie = State()  # стейт новичка
    newbie_knowledge_base = State()
    newbie_articles_info = State()
    newbie_knowledge_choose = State()
    newbie_q1 = State()
    newbie_q2 = State()
    newbie_q3 = State()
    newbie_q4 = State()
    newbie_q5 = State()
    newbie_q6 = State()
    newbie_q7 = State()
    newbie_q8 = State()
    newbie_q9 = State()
    newbie_q10 = State()
    newbie_test_result = State()
    newbie_choose_after_test = State()
    alliance_enter_or_webinar = State()
    webinar_reg_start = State()
    webinar_user_name = State()
    webinar_user_email = State()
    webinar_user_number = State()
    webinar_user_time = State()
    notfiy_not_active = State()
