
# from api.services import *
import os
from api import create_app
from dotenv import load_dotenv
# app = Flask(__name__)
load_dotenv()
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
config = {
    "username": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PWD"),
    "server": os.getenv("SERVER"),
    "db_name": os.getenv("DB_NAME")

}
app = create_app(config)

# app.add_url_rule("/assetScraper/api/getAssetInfo&name=<asset_name>", "/getStockAPI/<asset_name>",get_asset_info)
# app.add_url_rule()
if __name__ == "__main__":
    app.run(debug=True)