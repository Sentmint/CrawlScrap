
from  flask import Flask, redirect 
from api.database import Mongo
def create_app(config_obj):
    app = Flask(__name__)
    for k,v in config_obj.items():
        app.config[k] = v
    api_prefix = "/assetscraper/api/"
    app.db = Mongo()
    print(app.db.test)
    app.db.connect(app.config)
    from api.services import asset_request_routes, general_routes, error_handler_routes
    app.register_error_handler(404,error_handler_routes.unknown_page)
    app.register_blueprint(asset_request_routes.asset_req_route, url_prefix = api_prefix )
    app.register_blueprint(general_routes.general_route)
     
    return app