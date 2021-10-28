from .api import load_api_routes

def load_all_routes(app, *args, **kwargs):
    load_api_routes(app, *args, **kwargs)