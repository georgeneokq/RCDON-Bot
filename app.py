import os
from dotenv import load_dotenv
from flask import Flask
from routes.routes import load_all_routes
from modules.rcdon_bot import RCDONBot
from threading import Thread

# Load environment variables from .env file
load_dotenv('.env')

# Start the telegram bot
rcdon_bot = RCDONBot(os.getenv('BOT_TOKEN'))

# Create flask app instance
app = Flask(__name__)

# Load the API routes.
load_all_routes(app)

if __name__ == '__main__':
    print('Starting flask app and telegram bot, press Ctrl+C twice to terminate the program.')
    app.run()
    # print('Flask app stopped, press Ctrl+C to stop the bot. This may take some time, spam Ctrl+C and ENTER key to speed up the process.')
    rcdon_bot.updater.idle()
