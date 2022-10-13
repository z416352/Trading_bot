from datetime import datetime, timedelta
import sqlite3
import requests
import pandas as pd
import time
from exceptions import *
import sys

def get_candle_data(exchange = "binance", interval = "h1", baseId = "bitcoin", quoteId = "tether", start = datetime.now(), end = datetime.now()):
    print("get_candle_data() 爬取中....")

    ## interval = m1, m5, m15, m30, h1, h2, h6, h12, d1
    assert interval in {'m1', 'm5', 'm15', 'm30', 'h1', 'h2', 'h6', 'h12', 'd1'}, "interval error"

    start = (str)(time.mktime(start.timetuple()) * 1000)
    end = (str)(time.mktime(end.timetuple()) * 1000)
    url = f"http://api.coincap.io/v2/candles?exchange={exchange}&interval={interval}&baseId={baseId}&quoteId={quoteId}&start={start}&end={end}"
    payload={}
    headers = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if ("error" in response.json()) | ("data" not in response.json()):
            raise MessageErrorException("ERR: Price data message error(check url, ...)", url)

        crypto_price_data_list = response.json()["data"]
        if crypto_price_data_list == []:
            raise MessageEmptyException("ERR: Price data is empty(check start/end time)", start, end)

    except MessageErrorException as e:
        print(e)
        sys.exit(1)
    except MessageEmptyException as e:
        print(e)
        sys.exit(1)
    else:
        print("get_candle_data() 爬取成功 !")
    

    # convert list to dataframe
    df = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
    for crypto_dict in crypto_price_data_list:
        df.loc[datetime.fromtimestamp(crypto_dict["period"] / 1000)] = [
            crypto_dict["open"],
            crypto_dict["high"],
            crypto_dict["low"],
            crypto_dict["close"],
            crypto_dict["volume"]
        ]
    df = df.astype(float)
    df.round(2)
    
    return df

# 建立table
# def create_table(cursor, coin_name):
#     command = '''CREATE TABLE if not exists '{}' (
# 	"cid"	 INTEGER NOT NULL,
# 	"open"	 INTEGER,
# 	"high"	 INTEGER,
# 	"low"	 INTEGER,
# 	"close"	 INTEGER,
# 	"volume" INTEGER,
#     "date"   TEXT ,
# 	PRIMARY KEY("cid" AUTOINCREMENT)
#     );'''.format(coin_name)

#     cursor.execute(command)

# # 新增資料
# def insert_data(cursor, coin_table, open_price, high_price, low_price, close_price, volume, date_time):
#     command = "insert into '{}'(open, high, low, close, volume, date) values('{}', '{}', '{}', '{}', '{}', '{}');".format(coin_table, open_price, high_price, low_price, close_price, volume, date_time)
#     cursor.execute(command)


class DB_table():
    def __init__(self, db_name, coin_name):
        self.db_name = db_name
        self.coin_name = coin_name
        self.conn = None
        self.cursor = None

    # 初始化db
    def init_db(self):
        db_file = self.db_name
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    # 建立table by chih
    def create(self):
        command = '''CREATE TABLE if not exists '{}' (
        "Timestamp"	 TEXT NOT NULL,
        "Open"	 INTEGER,
        "High"	 INTEGER,
        "Low"	 INTEGER,
        "Close"	 INTEGER,
        "Volume" INTEGER,
        PRIMARY KEY("Timestamp")
        );'''.format(self.coin_name)
        
        self.cursor.execute(command)

    def update(self, interval):
        print("update() 處理中....")

        last_data_df = pd.read_sql("SELECT * FROM "+ self.coin_name +" WHERE Timestamp=(SELECT MAX(Timestamp) FROM " + self.coin_name +")", self.conn)

        last_date =  datetime.strptime(last_data_df['Timestamp'][0], '%Y-%m-%d %H:%M:%S')
        start = last_date + timedelta(seconds=3) # 避免重複資料的問題
        end = datetime.now()
        crypto_df = get_candle_data(start=start, end=end, interval=interval)

        try :
            crypto_df.to_sql(self.coin_name, self.conn, if_exists='append', index=True, index_label='Timestamp') 
        except sqlite3.IntegrityError:
            print("ERR: 可能有重複的資料")
            sys.exit(1)
        except Exception:
            print ("ERR: 其他錯誤")
            sys.exit(1)
        else:
            # print("From: " + start)
            # print("To: " + end)
            print("update() 新增完成 !")

    def show(self):
        df = pd.read_sql("SELECT * FROM "+ self.coin_name, self.conn)
        print(df)