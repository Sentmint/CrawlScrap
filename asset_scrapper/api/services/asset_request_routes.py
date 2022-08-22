from api.database import Mongo
import yfinance as yf
import pandas as pd
from flask import Blueprint, abort, g, jsonify, request, current_app

"""
GLOBAL 
Need to have asset_ticker query argument
"""

asset_req_route = Blueprint("asset_req_route", __name__)
accepted_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd']
accepted_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


@asset_req_route.before_request
def check_request():
    ticker = create_ticker(request.args, "asset_ticker")
    # if(not request.args.get("asset_ticker")):
        # return "Not valid value", 400
    if(not ticker):
        abort(status=400)
    g.ticker:yf.Ticker = ticker

    



@asset_req_route.route("/assetinfo")
def get_asset_info():
    result = current_app.db.push_data("general_info", g.ticker.info)
    return jsonify(data=g.get("ticker").info), 200
        

#This route DOESN'T WORK
@asset_req_route.route("/assetdividends")
def get_asset_dividends():
    return jsonify(g.get("ticker").get_dividends().to_json()), 200



@asset_req_route.route("/assethistory")
def get_asset_history():
    """
    :query_arg: period     This is the period of the history looking for, such as 1d, 1mo, etc
    :query_arg: interval   This is the interval between data points, such as 1m, 1h, 1wk, etc
    """
    args = request.args
    if args.get("period") not in accepted_periods and args.get("interval") not in accepted_intervals:
        return "Invalid period or interval", 400
    return jsonify((g.get("ticker").history(period=args.get("period"), interval=args.get("interval"))).to_json()), 200

#This route DOESN'T WORK
@asset_req_route.route("/assetsplits")
def get_asset_splits():      
    return jsonify(g.get("ticker").splits.to_json()), 200

@asset_req_route.route("/assetmajorholders")
def get_asset_major_holders():
    return jsonify(g.get("ticker").major_holders.to_json()), 200

@asset_req_route.route("/assetinstitutionalholders")
def get_asset_institutional_holders():
    return jsonify(g.get("ticker").institutional_holders.to_json()), 200

@asset_req_route.route("/assetfinancials")
def get_asset_financials():
    return jsonify(g.get("ticker").financials.to_json()), 200
    # print(yf.Ticker(asset_ticker).quarterly_financials)

@asset_req_route.route("/assetbalancesheet")
def get_asset_balance_sheet():
    return jsonify(g.get("ticker").balance_sheet.to_json()), 200
    # print(yf.Ticker(asset_ticker).quarterly_balance_sheet)

@asset_req_route.route("/assetcashflow")
def get_asset_cash_flow():
    return jsonify(g.get("ticker").cashflow.to_json()), 200

@asset_req_route.route("/assetearnings")
def get_asset_earning():
    return jsonify(g.get("ticker").earnings.to_json()), 200


@asset_req_route.route("/assetsustainability")
def get_asset_sustainability():
    return jsonify(g.get("ticker").sustainability.to_json()), 200

@asset_req_route.route("/assetrecommendation")
def get_asset_recommendation():
    """
    Summary:
    Shows analysts reccomendations

    """
    return jsonify(g.get("ticker").recommendations.to_json()), 200


#Handle bad request errors, usually incorrect query parameters or values
@asset_req_route.errorhandler(400)
def handle_bad_request(e):
    # g.db.close() Should routes close it's own db connections?
    return "Bad request!", 400

def create_ticker(args, ticker_name) -> yf.Ticker:
    tick_obj = yf.Ticker(args.get(ticker_name))
    if ticker_name == None or len(tick_obj.history()) == 0:
        return None
    return tick_obj


        
    