from telegram import Update


async def help_command(update: Update):
    help_text = """
📖 Доступные команды:

🎬 Фильмы:
/add_movie - Добавить фильм
/my_movies - Мои фильмы
/mark_watched - Отметить как просмотренный

📂 Плейлисты:
/create_playlist - Создать плейлист
/my_playlists - Мои плейлисты
/add_to_playlist - Добавить фильм в плейлист

🔍 Поиск:
/search_movie - Найти фильм
/recommend - Получить рекомендацию

📊 Статистика:
/stats - Моя статистика
    """

    await update.message.reply_text(help_text)