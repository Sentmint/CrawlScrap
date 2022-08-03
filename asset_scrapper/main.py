
# from api.services import *
from api import create_app
# app = Flask(__name__)

# api_prefix = "/assetscraper/api/"




# @app.route("/")
# def index():
#     return redirect("/assetscraper/api/")



# app.register_error_handler(404,unknown_page)

# app.register_blueprint(asset_req_api, url_prefix = api_prefix)

# def create_app(config_obj):
#     app = Flask(__name__)
#     app.config.from_object(config_obj)
#     from api.services import asset_request_routes
#     app.register_error_handler(404,unknown_page)
#     app.register_blueprint(asset_request_routes.asset_req_route, url_prefix = api_prefix)
     
#     return app

app = create_app({"some_config": "test"})

# app.add_url_rule("/assetScraper/api/getAssetInfo&name=<asset_name>", "/getStockAPI/<asset_name>",get_asset_info)
# app.add_url_rule()
if __name__ == "__main__":
    app.run(debug=True)