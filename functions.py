from datetime import datetime
import sqlite3
import requests
import pandas as pd
import time

def millisecond2date(milliseconds):
    timestamp = milliseconds / 1000
    value = datetime.fromtimestamp(timestamp)

    return value

def date2millisecond(date_time):
    return (int)(time.mktime(date_time.timetuple()) * 1000)


def get_candle_data(exchange = "binance", interval = "d1", baseId = "bitcoin", quoteId = "tether", start = datetime.now(), end = datetime.now()):
    ## interval = m1, m5, m15, m30, h1, h2, h6, h12, d1
    assert interval in {'m1', 'm5', 'm15', 'm30', 'h1', 'h2', 'h6', 'h12', 'd1'}, "interval error"

    start = (str)(date2millisecond(start))
    end = (str)(date2millisecond(end))
    url = "http://api.coincap.io/v2/candles?"+\
            "exchange="+exchange+ \
            "&interval="+interval+ \
            "&baseId="+baseId+ \
            "&quoteId="+quoteId+ \
            "&start="+start+ \
            "&end="+end	

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    assert not(("error" in response.json()) | ("data" not in response.json())), "price data message error(check url, ...)"
    
    crypto_price_data_list = response.json()["data"]
    assert crypto_price_data_list, "price data is empty(check start/end time)"
    
    # convert list to dataframe
    df = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
    for crypto_dict in crypto_price_data_list:
        df.loc[millisecond2date(crypto_dict["period"])] = [
            crypto_dict["open"],
            crypto_dict["high"],
            crypto_dict["low"],
            crypto_dict["close"],
            crypto_dict["volume"]
        ]
    df = df.astype(float)
    df.round(2)
    
    return df

# 初始化db
def init_db(db_name):
    db_file = db_name
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    return cursor, conn

# 建立table
def create_table(cursor, coin_name):
    command = '''CREATE TABLE if not exists '{}' (
	"cid"	 INTEGER NOT NULL,
	"open"	 INTEGER,
	"high"	 INTEGER,
	"low"	 INTEGER,
	"close"	 INTEGER,
	"volume" INTEGER,
    "date"   TEXT ,
	PRIMARY KEY("cid" AUTOINCREMENT)
    );'''.format(coin_name)

    cursor.execute(command)

# 新增資料
def insert_data(cursor, coin_table, open_price, high_price, low_price, close_price, volume, date_time):
    command = "insert into '{}'(open, high, low, close, volume, date) values('{}', '{}', '{}', '{}', '{}', '{}');".format(coin_table, open_price, high_price, low_price, close_price, volume, date_time)
    cursor.execute(command)
