
from flask import Blueprint, current_app, redirect

general_route = Blueprint("general_route", __name__)


@general_route.route("/")
def index():
    return redirect("/assetscraper/api/")

@general_route.route("/assetscraper/api/")
def home():
    return "Welcome to StockTrack! Please look into the documentation for available routes. Thank you!"