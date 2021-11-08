from flask import request, Flask
from modules.db_users import DBUsers
from telegram.bot import Bot
from telegram.error import TelegramError
from os import getenv
import time

def load_api_routes(app: Flask, *args, **kwargs) -> None:
    """
    Params:
        app - The main flask app instance

    This function loads the API routes when called.
    """
    # bot: RCDONBot = kwargs['bot']
    bot = Bot(getenv('BOT_TOKEN'))

    db_users = DBUsers('data/users.csv')

    @app.route('/api/can-kms', methods=['POST'])
    def can_kms():
        """
        For client to poll as a kill switch

        Request body:
            "key" - API key

        Possible responses:
            "true" - Can kys
            "false" - Cannot kys
            "invalid" - Invalid key
        """
        key = request.json['key']

        while True:
            time.sleep(0.2)
            # Retrieve by key
            record = db_users.get_by_key(key)

            if not record:
                return "invalid"

            can_kill = str(bool(int(record['can_kill']))).lower()

            # print(prev_state != can_kill)
            if(can_kill == "true"):
                break

        return can_kill


    @app.route('/api/always-can-kms', methods=['POST'])
    def always_can_kms():
        """
        For client to poll as a kill switch, always returns true. For testing purposes only.

        Request body: -

        Possible responses:
            "true"
        """
        return "true"

    @app.route('/api/report/breach', methods=['POST'])
    def report_breach():
        """
        Receive reports of unauthorized usage of devices.
        Send a message to the telegram bot associated with the key

        Request body:
            "key" - API key
            "message" - Message to be send to the telegram bot

        Possible responses:
            "true" - The message was successfully sent to the client
            "false" - Some error occurred while sending message to the client
        """
        key = request.json.get('key')
        message = request.json.get('message')

        # Get user by key, send message to associated user
        user: dict = db_users.get_by_key(key)
        if user.get('user_id') is None:
            return "false"

        print(f'Sending message to {user.get("username")} (chat id {user.get("user_id")})')
        try:
            bot.send_message(user.get('user_id'), message)
        except TelegramError as e:
            print('Unexpected error occurred while sending the message to the user.')
            return "false"

        return "true"

    # Report that the device has been unblocked. Toggle can_kill switch in database
    @app.route('/api/report/unblock', methods=['POST'])
    def report_unblock():
        """
        For client to report that the client has been successfully unblocked.
        The kill switch for the client will be reset.

        Request body:
            "key" - API key

        Possible responses:
            "true" - Kill switch update success
            "invalid" - Invalid key
        """
        # Update CSV file
        key = request.json.get('key')

        # Reset the kill switch
        success = db_users.edit_record('key', key, 'can_kill', 0)

        if not success:
            return "invalid"

        return "true"
