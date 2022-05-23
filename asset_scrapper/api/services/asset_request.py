import yfinance as yf

def get_asset_info(asset_name: str):
    return yf.Ticker(asset_name).info

def get_asset_dividends(asset_name: str):
    return yf.Ticker(asset_name).dividends

def get_asset_history(asset_name: str, period: str = "str", interval: str = "1d"):
    return yf.Ticker(asset_name).history(period=period, interval=interval)

def get_asset_splits(asset_name: str):
    return yf.Ticker(asset_name).splits

def get_asset_major_holders(asset_name: str):
    return yf.Ticker(asset_name).major_holders

def get_asset_institutional_holders(asset_name: str):
    return yf.Ticker(asset_name).institutional_holders

def get_asset_financials(asset_name: str):
    print(yf.Ticker(asset_name).financials)
    print(yf.Ticker(asset_name).quarterly_financials)

def get_asset_balance_sheet(asset_name: str):
    print(yf.Ticker(asset_name).balance_sheet)
    print(yf.Ticker(asset_name).quarterly_balance_sheet)
    
def get_asset_cash_flow(asset_name: str):
    print(yf.Ticker(asset_name).cash_flow)
    print(yf.Ticker(asset_name).quarterly_cashflow)

def get_asset_earning(asset_name: str):
    print(yf.Ticker(asset_name).earnings)
    print(yf.Ticker(asset_name).quarterly_earnings)
    
def get_asset_sustainability(asset_name: str):
    return yf.Ticker(asset_name).sustainability
    
def get_asset_recommendation(asset_name: str): #Shows analysts reccomendations
    return yf.Ticker(asset_name).recommendations
    

