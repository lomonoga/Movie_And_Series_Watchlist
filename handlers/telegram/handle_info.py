from telegram import Update
from telegram.ext import ContextTypes

from handlers.telegram.keyboards.menu_keyboard import get_menu_keyboard


async def handle_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = """
📖 Доступные разделы:

🎬 Фильмы и сериалы
• Добавить фильм или сериал
• Просмотреть мои фильмы и сериалы
• Оценить фильм или сериал
• Отметить фильм или сериал просмотренным
• Удалить фильм или сериал

📂 Плейлисты
• Создать плейлист
• Просмотреть плейлисты
• Добавить фильм или сериал в плейлист
• Просмотреть список фильмов и сериалов в плейлисте  

🎯 Рекомендации:
• Получить рекомендацию по просмотру фильма из вашего списка
    """

    if update.message is not None:
        await update.message.delete()
        await update.message.reply_text(
            info_text,
            reply_markup=get_menu_keyboard(),
            parse_mode='HTML'
        )
    elif update.callback_query is not None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            info_text,
            reply_markup=get_menu_keyboard(),
            parse_mode='HTML'
        )
