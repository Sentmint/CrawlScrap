import flask
from api import get_asset_info
app = flask.Flask(__name__)

app.add_url_rule("/getStock/<asset_name>", "/getStock/<asset_name>",get_asset_info)

if __name__ == "__main__":
    app.run(debug=True)