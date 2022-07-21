from  flask import Flask 
from api.services import *
app = Flask(__name__)

api_prefix = "/assetscraper/api/"

def unknown_page(e):
    return "this route doesn't eixst", 404


app.register_error_handler(404,unknown_page)


app.register_blueprint(asset_req_api, url_prefix = api_prefix)

# app.add_url_rule("/assetScraper/api/getAssetInfo&name=<asset_name>", "/getStockAPI/<asset_name>",get_asset_info)
# app.add_url_rule()
if __name__ == "__main__":
    app.run(debug=True)