from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Создает главную клавиатуру меню."""
    buttons = [
        [InlineKeyboardButton(text="❓ FAQ", callback_data="show_faq")],
        [InlineKeyboardButton(text="🎓 Программы обучения", callback_data="show_programs")],
        [InlineKeyboardButton(text="📝 Шаги подачи документов", callback_data="show_guide")],
        [InlineKeyboardButton(text="✅ Список документов", callback_data="check_docs")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="show_contacts")],
        [InlineKeyboardButton(text="🔍 Задать вопрос", callback_data="ask_question")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой возврата в главное меню."""
    buttons = [
        [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
