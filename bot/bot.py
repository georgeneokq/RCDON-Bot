from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os
from threading import Thread

class RCDONBot:
    """
    Class representing the telegram bot.
    Contains callback handlers as well.

    To get user details, use update.effective_user, which has the following fields (so far discovered).
    id, username, is_bot, first_name, language_code
    """
    def __init__(self):
        """
        Perform configuration and start the bot
        """
        # Enable logging
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(message)s', level=logging.INFO
        )

        self.logger = logging.getLogger(__name__)

        self.initialize_bot()

    def initialize_bot(self):
        """ Start the bot """
        self.updater = Updater(os.getenv('BOT_TOKEN'))

        # Get dispatcher to register handlers
        dispatcher = self.updater.dispatcher

        # Register callback handlers to handle telegram messages
        dispatcher.add_handler(CommandHandler("handle_start", self.handle_start))
        dispatcher.add_handler(CommandHandler("handle_help", self.handle_help))
        
        # On non-command i.e. message
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))

        # Start the bot, non-blocking
        self.updater.start_polling()

    def stop(self):
       """
       Stops the polling/webhook thread, the dispatcher and the job queue.
       """
       self.updater.stop()

    def handle_start(self, update: Update, context: CallbackContext) -> None:
        """
        /start

        prompt for user information.
        Try checking for phone number, goodware should ask for phone number
        """
        user = update.effective_user
        print(user)
        update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True)
        )

    def handle_help(self, update: Update, context: CallbackContext):
        """
        /help

        Send help message
        """
        update.message.reply_text("Under maintenance")

    def handle_message(self, update: Update, context: CallbackContext):
        user = update.effective_user
        update.message.reply_text(f'Back to {user.username}: {update.message.text}')