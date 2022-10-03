from datetime import datetime
import requests

def millisecond2date(milliseconds):
    timestamp = milliseconds / 1000
    value = datetime.fromtimestamp(timestamp)
    
    return value

def get_candle_data(exchange = "binance", interval = "d1", baseId = "bitcoin", quoteId = "tether"):
    ## interval = m1, m5, m15, m30, h1, h2, h6, h12, d1
    if interval not in {'m1', 'm5', 'm15', 'm30', 'h1', 'h2', 'h6', 'h12', 'd1'}:
        print("interval error")
        return None

    url = "http://api.coincap.io/v2/candles?exchange="+exchange+"&interval="+interval+"&baseId="+baseId+"&quoteId="+quoteId

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    crypto_price_data_list = response.json()["data"]

    # print ("len = ", len(crypto_price_data_list))
    for i in range(len(crypto_price_data_list)):
        crypto_price_data_list[i]["period"] = millisecond2date(crypto_price_data_list[i]["period"])
        print(crypto_price_data_list[i])

    return crypto_price_data_list