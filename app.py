import os
from dotenv import load_dotenv
from flask import Flask
from routes.routes import load_all_routes
from modules.bot import RCDONBot
from threading import Thread

# Load environment variables from .env file
load_dotenv('.env')

# Start the telegram bot
bot = RCDONBot(os.getenv('BOT_TOKEN'))

# Create flask app instance
app = Flask(__name__)

# Load the API routes.
# The telegram bot is passed through kwargs
load_all_routes(app, bot=bot)

if __name__ == '__main__':
    print('Starting flask app and telegram bot, press Ctrl+C twice to terminate the program.')
    app.run()
    print('Flask app stopped, press Ctrl+C one more time to stop the bot.')
    bot.updater.idle()