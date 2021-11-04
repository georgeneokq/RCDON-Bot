from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from modules.db_users import DBUsers

class RCDONBot:
    """
    Class that wraps the handlers for the telegram bot.
    Sending messages are done using the telegram.Bot class that comes with python-telegram-bot package.

    To get user details, use update.effective_user, which has the following fields (so far discovered).
    id, username, is_bot, first_name, language_code
    """
    def __init__(self, token):
        """
        Perform configuration and start the bot
        """
        self.token = token

        self.initialize_bot()

    def initialize_bot(self):
        """ Start the bot """
        self.updater = Updater(self.token)

        # Get dispatcher to register handlers
        dispatcher = self.updater.dispatcher

        # Register callback handlers to handle telegram messages.
        # Methods declared in this class with the prefix "handle_command"
        # will automatically be registered as a command handler.
        class_fields = dir(self)
        
        for i in range(len(class_fields) - 1, -1, -1):
            class_field = class_fields[i]

            if class_field.startswith('__'):
                break
        
            if class_field.startswith('handle_command'):
                field_parts = class_field.split('_')
                command_name = '_'.join(field_parts[2:])
                dispatcher.add_handler(CommandHandler(command_name, getattr(self, class_field)))
                print(f'Registered handler for /{command_name} with function {class_field}')
        
        
        # On non-command i.e. message
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))

        # Start the bot, non-blocking
        self.updater.start_polling()

    def stop(self):
       """
       Stops the polling/webhook thread, the dispatcher and the job queue.
       """
       self.updater.stop()
       self.updater.is_idle = False

    def handle_command_start(self, update: Update, context: CallbackContext) -> None:
        """
        /start

        prompt for user information.
        Try checking for phone number, goodware should ask for phone number
        """
        user = update.effective_user
        
        user_id = user.id
        db_users = DBUsers('data/users.csv')
        user_record = db_users.get_by_username(user.username)
        
        if user_record is None:
            update.message.reply_text(f'Your telegram account is not registered with us.')
        else:
            db_users.edit_record('username', user.username, 'user_id', user_id)
            update.message.reply_text(
                f'Hi {user.username}! You can now receive notifications from me.',
                reply_markup=ForceReply(selective=True)
            )


    def handle_command_help(self, update: Update, context: CallbackContext) -> None:
        """
        /help

        Send help message
        """
        update.message.reply_text("Under maintenance")

    def handle_message(self, update: Update, context: CallbackContext):
        user = update.effective_user
        update.message.reply_text(f'Back to {user.username}: {update.message.text}')


# For testing only
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv('../.env')
    token = os.getenv('BOT_TOKEN')
    bot = RCDONBot(token)
    bot.updater.idle()