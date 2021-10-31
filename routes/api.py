from flask import request

def load_api_routes(app, *args, **kwargs):
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