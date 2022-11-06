from datetime import datetime, timedelta
import sqlite3
import pandas as pd
from exceptions import *
import sys
from crypto_backtrader.finlab import crypto

# def get_candle_data(exchange = "binance", interval = "h1", baseId = "bitcoin", quoteId = "tether", start = datetime.now(), end = datetime.now()):
#     print("get_candle_data() 爬取中....")

#     ## interval = m1, m5, m15, m30, h1, h2, h6, h12, d1
#     assert interval in {'m1', 'm5', 'm15', 'm30', 'h1', 'h2', 'h6', 'h12', 'd1'}, "interval error"

#     start = (str)(time.mktime(start.timetuple()) * 1000)
#     end = (str)(time.mktime(end.timetuple()) * 1000)
#     url = f"http://api.coincap.io/v2/candles?exchange={exchange}&interval={interval}&baseId={baseId}&quoteId={quoteId}&start={start}&end={end}"
#     payload={}
#     headers = {}

#     try:
#         response = requests.request("GET", url, headers=headers, data=payload)
#         if ("error" in response.json()) | ("data" not in response.json()):
#             raise MessageErrorException("ERR: Price data message error(check url, ...)", url)

#         crypto_price_data_list = response.json()["data"]
#         if crypto_price_data_list == []:
#             raise MessageEmptyException("ERR: Price data is empty(check start/end time)", start, end)

#     except MessageErrorException as e:
#         print(e)
#         sys.exit(1)
#     except MessageEmptyException as e:
#         print(e)
#         sys.exit(1)
#     else:
#         print("get_candle_data() 爬取成功 !")
    
#     # convert list to dataframe
#     df = pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"])
#     for crypto_dict in crypto_price_data_list:
#         df.loc[datetime.fromtimestamp(crypto_dict["period"] / 1000)] = [
#             crypto_dict["open"],
#             crypto_dict["high"],
#             crypto_dict["low"],
#             crypto_dict["close"],
#             crypto_dict["volume"]
#         ]
#     df = df.astype(float)
#     df.round(2)
    
#     return df

def get_price_data(Trading_pair='BTCUSDT', Interval='1d', start=datetime.strptime('1 Jan 2017', '%d %b %Y'), end=datetime.now()):
    time_frame = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "1d"]
    if Interval in time_frame:
        df = crypto.get_all_binance(Trading_pair, Interval, save=False, start=start)
        df = df.drop(["Close_time", "Quote_av", "Trades", "Tb_base_av", "Tb_quote_av", "Ignore"], axis=1)
        df = df.reset_index(level=0)

        # utc+8
        df['Timestamp'] += timedelta(hours=8)
    else:
        print("ERR: Time frame does not match:", Interval)
        print(" Enter this time frame:", time_frame)
        exit(1)

    return df

class DB_table():
    def __init__(self, db_file_path, coin_name):
        self.db_file_path = db_file_path
        self.coin_name = coin_name
        self.conn = None
        self.cursor = None

    # 初始化db
    def init_db(self):
        db_file = self.db_file_path
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

    def update(self, Interval):
        print("----> update() 處理中....")

        last_data_df = pd.read_sql("SELECT * FROM "+ self.coin_name +" WHERE Timestamp=(SELECT MAX(Timestamp) FROM " + self.coin_name +")", self.conn)
        if not last_data_df.empty:
            last_date =  datetime.strptime(last_data_df['Timestamp'][0], '%Y-%m-%d %H:%M:%S')
            start = last_date + timedelta(seconds=1) # 避免重複資料的問題
            print("     last_date =", last_date)
        else: start = datetime.strptime('1 Jan 2017', '%d %b %Y')

        crypto_df = get_price_data(Interval=Interval, start=start)

        try :
            # crypto_df.to_sql(self.coin_name, self.conn, if_exists='append', index=True, index_label='Timestamp') 
            crypto_df.to_sql(self.coin_name, self.conn, if_exists='append', index=False) 
        except sqlite3.IntegrityError:
            print("ERR: 可能有重複的資料")
            sys.exit(1)
        except Exception:
            print ("ERR: 其他錯誤")
            sys.exit(1)
        else:
            # print("From: " + start)
            # print("To: " + end)
            print("----> update() 新增完成 !")
    

    def get_all(self):
        df = pd.read_sql("SELECT * FROM "+ self.coin_name, self.conn)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df

