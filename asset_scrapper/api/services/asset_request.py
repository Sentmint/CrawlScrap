import yfinance as yf
import pandas as pd
from flask import Blueprint, abort, g, jsonify, make_response, request

"""
GLOBAL 
Need to have asset_ticker query argument
"""






asset_req_api = Blueprint("asset_req_api", __name__)
accepted_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd']
accepted_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']


@asset_req_api.before_request
def check_request():
    ticker = create_ticker(request.args, "asset_ticker")
    # if(not request.args.get("asset_ticker")):
        # return "Not valid value", 400
    if(not ticker):
        abort(status=400)
    g.ticker = ticker
    



@asset_req_api.route("/assetinfo")
def get_asset_info():
    args = request.args
    # ticker = create_ticker(args,"asset_ticker")
    # if(not ticker):
    #     return handle_ticker_error(ticker)
    return jsonify(g.get("ticker").info), 200
        


@asset_req_api.route("/assetdividends")
def get_asset_dividends():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)
    return jsonify(ticker.dividends), 200



@asset_req_api.route("/assethistory")
def get_asset_history():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)
    elif(args.get("period") not in accepted_periods and args.get("interval") not in accepted_intervals):
        return "Invalid period or interval", 400
    return jsonify((ticker.history(period=args.get("period"), interval=args.get("interval"))).to_json()), 200

@asset_req_api.route("/assetsplits")
def get_asset_splits():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)       
    return jsonify(ticker.splits), 200

@asset_req_api.route("/assetmajorholders")
def get_asset_major_holders():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)      
    return jsonify(ticker.major_holders.to_json()), 200

@asset_req_api.route("/assetinstitutionalholders")
def get_asset_institutional_holders():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return jsonify(ticker.institutional_holders.to_json()), 200

@asset_req_api.route("/assetfinancials")
def get_asset_financials():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return jsonify(ticker.financials.to_json()), 200
    # print(yf.Ticker(asset_ticker).quarterly_financials)

@asset_req_api.route("/assetbalancesheet")
def get_asset_balance_sheet():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return jsonify(ticker.balance_sheet.to_json()), 200
    # print(yf.Ticker(asset_ticker).quarterly_balance_sheet)

@asset_req_api.route("/assetcashflow")
def get_asset_cash_flow():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return jsonify(ticker.cashflow.to_json()), 200
    # print(yf.Ticker(asset_ticker).cash_flow)
    # print(yf.Ticker(asset_ticker).quarterly_cashflow)

@asset_req_api.route("/assetearnings")
def get_asset_earning():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return jsonify(ticker.earnings.to_json()()), 200
    # print(yf.Ticker(asset_ticker).earnings)
    # print(yf.Ticker(asset_ticker).quarterly_earnings)

@asset_req_api.route("/assetsustainability")
def get_asset_sustainability():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)
    return jsonify(ticker.sustainability.to_json()), 200
    # return yf.Ticker(asset_ticker).sustainability

@asset_req_api.route("/assetrecommendation")
def get_asset_recommendation(): #Shows analysts reccomendations
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)
    print(ticker.recommendations.to_json())
    return jsonify(ticker.recommendations.to_json()), 200


#To handle errors here if need be
@asset_req_api.errorhandler(400)
def handle_bad_request(e):
    return "Bad request!", 400

def create_ticker(args, ticker_name):
    tick_obj = yf.Ticker(args.get(ticker_name))
    if(ticker_name == None or len(tick_obj.history()) == 0):
        return None
    return tick_obj


#Could add more logic in the future
def handle_ticker_error(ticker):
    if(ticker == None):
        return "Not a valid ticker", 400
        
    