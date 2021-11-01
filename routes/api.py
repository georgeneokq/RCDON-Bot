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

        TODO: Think of how to work with the binary
        """
        print(request.form)
        
        response = {
            "err": 0,
            "msg": "ok"
        }

        return response

    # Report that the device has been unblocked. Toggle can_kill switch in database
    @app.route('/api/report/unblock', methods=['POST'])
    def report_unblock():
        # Update CSV file
        key = request.form.get('key')

        # Reset the kill switch
        db_users.edit_record('key', key, 'can_kill', 0)
        
        response = {
            "err": 0,
            "msg": "ok"
        }

        return response

    @app.route('/api/can_kms', methods=['POST'])
    def can_kms():
        key = request.form['key']

        # Retrieve by key
        record = db_users.get_by_key(key)
        
        if record is None:
            return {
                "err": 1,
                "msg": "Invalid key"
            }
        
        can_kill = int(record['can_kill'])
        
        return {
            "err": 0,
            "msg": "ok",
            "data": {
                "can_kill": can_kill
            }
        }


    @app.route('/api/always_can_kms', methods=['POST'])
    def always_can_kms():
        """ For client to poll as a kill switch """
        response = {
            "err": 0,
            "msg": "ok",
            "data": {
                "can_kill": 1
            }
        }

        return response
