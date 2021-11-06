from .api import load_api_routes
from .web import load_web_routes

def load_routes(app, *args, **kwargs):
    load_api_routes(app, *args, **kwargs)
    load_web_routes(app, *args, **kwargs)