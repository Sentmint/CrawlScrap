import yfinance as yf
import pandas as pd
from flask import Blueprint, jsonify, make_response, request

asset_req_api = Blueprint("asset_req_api", __name__)
accepted_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd']
accepted_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
@asset_req_api.route("/assetinfo")
def get_asset_info():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)
    return jsonify(ticker.info), 200
        


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
    return ticker.splits

@asset_req_api.route("/assetmajorholders")
def get_asset_major_holders():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)      
    return ticker.major_holders

@asset_req_api.route("/assetinstitutionalholders")
def get_asset_institutional_holders():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return ticker.institutional_holders

def get_asset_financials(asset_ticker: str):
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return ticker.financials
    # print(yf.Ticker(asset_ticker).quarterly_financials)

def get_asset_balance_sheet():
    args = request.args
    ticker = create_ticker(args,"asset_ticker")
    if(not ticker):
        return handle_ticker_error(ticker)  
    return ticker.balance_sheet
    # print(yf.Ticker(asset_ticker).quarterly_balance_sheet)
    
def get_asset_cash_flow(asset_ticker: str):
    print(yf.Ticker(asset_ticker).cash_flow)
    print(yf.Ticker(asset_ticker).quarterly_cashflow)

def get_asset_earning(asset_ticker: str):
    print(yf.Ticker(asset_ticker).earnings)
    print(yf.Ticker(asset_ticker).quarterly_earnings)
    
def get_asset_sustainability(asset_ticker: str):
    return yf.Ticker(asset_ticker).sustainability
    
def get_asset_recommendation(asset_ticker: str): #Shows analysts reccomendations
    return yf.Ticker(asset_ticker).recommendations
    


#To handle errors here if need be
# @asset_req_api.app_errorhandler(400)
# def missing_query(e):
#     res = make_response(e)
#     print(e)
#     return e

def create_ticker(args, ticker_name):
    tick_obj = yf.Ticker(args.get(ticker_name))
    if(ticker_name == None or len(tick_obj.dividends) == 0):
        return None
    return tick_obj


#Could add more logic in the future
def handle_ticker_error(ticker):
    if(ticker == None):
        return "Not a valid ticker", 400
        
    