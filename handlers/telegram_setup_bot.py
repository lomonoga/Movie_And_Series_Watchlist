from telegram.ext import Application, CommandHandler

from handlers.telegram.help_handler import help_command
from handlers.telegram.start_handler import start_command


def setup_bot(token: str) -> Application:
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # application.add_handler(MessageHandler(
    #     filters.StatusUpdate.NEW_CHAT_MEMBERS,
    #     handle_user_joined
    # ))
    # application.add_handler(MessageHandler(
    #     filters.StatusUpdate.LEFT_CHAT_MEMBER,
    #     handle_user_left
    # ))

    return application
