from flask import request, Flask
from modules.db_users import DBUsers

def load_api_routes(app: Flask, *args, **kwargs) -> None:
    """ 
    Params:
        app - The main flask app instance

    This function loads the API routes when called.
    """
    bot = kwargs['bot']
    db_users = DBUsers('data/users.csv')
    
    # Routes to "report"/update status
    # TODO: Maybe report a breach
    @app.route('/api/report/breach', methods=['POST'])
    def report_breach():
        """
        Receive reports of unauthorized usage of devices.
        Send a message to the telegram bot associated with the key

        TODO: Take message from the binary, send it to the associated telegram client as-is

        Possible responses:
            "true" - The message was successfully sent to the client
            "false" - Some error occurred while sending message to the client
        """
        print(request.form)
        
        return "true"

    # Report that the device has been unblocked. Toggle can_kill switch in database
    @app.route('/api/report/unblock', methods=['POST'])
    def report_unblock():
        """
        For client to report that the client has been successfully unblocked.
        The kill switch for the client will be reset.

        Possible responses:
            "true" - Kill switch update success
            "invalid" - Invalid key
        """
        # Update CSV file
        key = request.form.get('key')

        # Reset the kill switch
        success = db_users.edit_record('key', key, 'can_kill', 0)

        if not success:
            return "invalid"
        
        return "true"

    @app.route('/api/can-kms', methods=['POST'])
    def can_kms():
        """
        For client to poll as a kill switch

        Possible responses:
            "true" - Can kys
            "false" - Cannot kys
            "invalid" - Invalid key
        """
        key = request.form['key']

        # Retrieve by key
        record = db_users.get_by_key(key)
        
        if record is None:
            return "invalid"
        
        can_kill = str(bool(int(record['can_kill']))).lower()
        
        return can_kill


    @app.route('/api/always-can-kms', methods=['POST'])
    def always_can_kms():
        """
        For client to poll as a kill switch, always returns true. For testing purposes only.
        
        Possible responses:
            "true"
        """
        return "true"