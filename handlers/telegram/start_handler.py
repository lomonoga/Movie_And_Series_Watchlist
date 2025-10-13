from sqlalchemy.future import select
from telegram import Update
from telegram.ext import ContextTypes

from conf import Logger
from database.postgresql_database import get_async_db_session
from models.database.models_database import User


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            db_user.first_name = user.first_name or db_user.first_name
            Logger.info(f"User updated with id: {user.id}")
            await session.commit()

    welcome_text: str = f"""
👋 Привет, {user.first_name}!

Я твой бот для управления коллекцией фильмов и сериалов.

📝 Что я умею:
• Добавлять фильмы и сериалы в плейлисты
• Вести список просмотренных фильмов
• Рекомендовать что посмотреть
• Хранить твои оценки, а так же получать оценку фильмов из интернета

Начни с команды /help чтобы узнать больше!
    """

    await update.message.reply_text(welcome_text)
