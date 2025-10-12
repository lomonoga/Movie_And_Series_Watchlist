from telegram.ext import Application, Updater
from conf import Config

application = Application.builder().token(Config.BOT_TOKEN).build()
