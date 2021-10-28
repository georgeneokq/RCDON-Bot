from dotenv import load_dotenv
from flask import Flask
from routes.routes import load_all_routes
from bot.bot import RCDONBot
from threading import Thread

# Load environment variables from .env file
load_dotenv('.env')

# Start the telegram bot
bot = RCDONBot()

app = Flask(__name__)

# Load the API routes.
# The telegram bot is passed as through kwargs
load_all_routes(app, bot=bot)

bot.updater.idle()