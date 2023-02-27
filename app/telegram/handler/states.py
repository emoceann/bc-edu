from aiogram.dispatcher.filters.state import StatesGroup, State


class NewUser(StatesGroup):
    new_or_experienced = State()  # стейт новичок или продвинутый
    experienced = State()  # стейт продвинутого
    newbie = State()  # стейт новичка
    newbie_knowledge_base = State()
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
