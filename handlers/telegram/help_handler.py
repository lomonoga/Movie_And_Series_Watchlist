from telegram import Update
from telegram.ext import ContextTypes

from handlers.telegram.keyboards.main_menu_keyboard import get_menu_keyboard


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()

    help_text = """
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

    await update.message.reply_text(
        help_text,
        reply_markup=get_menu_keyboard(),
        parse_mode='HTML'
    )
