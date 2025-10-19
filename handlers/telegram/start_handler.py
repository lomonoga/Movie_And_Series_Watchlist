from sqlalchemy.future import select
from telegram import Update
from telegram.ext import ContextTypes

from conf import Logger
from database.postgresql_database import get_async_db_session
from handlers.telegram.keyboards.main_menu_keyboard import get_menu_keyboard
from models.database.models_database import User


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    user = update.effective_user

    Logger.info(f"User {user.id} started the bot")

    async with get_async_db_session() as session:
        result = await session.execute(select(User).where(User.id == user.id))
        db_user = result.scalar_one_or_none()

        if not db_user:
            db_user = User(
                id=user.id,
                is_bot=user.is_bot,
                first_name=user.first_name or "Unknown"
            )
            session.add(db_user)
            await session.commit()
            Logger.info(f"New user created with id: {user.id}")
        else:
            if user.first_name != db_user.first_name:
                db_user.first_name = user.first_name
                Logger.info(f"User updated with id: {user.id}")
                await session.commit()

    welcome_text: str = f"""
👋 Привет, {user.first_name}!

Я твой бот для управления коллекцией фильмов и сериалов.

📝 Что я умею:
• Добавлять фильмы и сериалы
• Управлять твоими плейлистами
• Вести список просмотренных фильмов
• Рекомендовать что посмотреть
• Хранить твои оценки, а так же получать оценку фильмов из интернета


👇 Выбери кнопку ниже и перестань терять фильмы!
    """

    await update.message.reply_text(
        welcome_text,
        reply_markup=get_menu_keyboard(),
        parse_mode='HTML'
    )
