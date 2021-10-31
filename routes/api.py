from flask import request, Flask

def load_api_routes(app: Flask, *args, **kwargs) -> None:
    """ 
    Params:
        app - The main flask app instance

    This function loads the API routes when called.
    """
    # TODO: Build more endpoints, integrate SQLite database
    bot = kwargs['bot']
    
    @app.route('/api/report/breach', methods=['POST'])
    def report_breach():
        print(request.json)
        
        response = {
            "err": 0,
            "msg": "ok"
        }

        return response

    @app.route('/api/can_kms', methods=['POST'])
    def can_kms():
        return "no"

    @app.route('/api/always_can_kms', methods=['POST'])
    def always_can_kms():
        """ For client to poll as a kill switch """
        print(request.json)

        response = {
            "err": 0,
            "msg": "ok",
            "data": {
                "can_kill": True
            }
        }

        return response