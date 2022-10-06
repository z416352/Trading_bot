from dis import findlabels
import requests
import sqlite3


from finlab import crypto

# {"1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "1d"}
df = crypto.get_all_binance('BTCUSDT', '1h', save=False)
df = df.drop(["Close_time", "Quote_av", "Trades", "Tb_base_av", "Tb_quote_av", "Ignore"], axis=1)
# print(df)

# dbfile = "test.db"
# conn = sqlite3.connect(dbfile)
# c = conn.cursor()

# # coin_txt 放入要存入的幣別
# coin_txt = open("coin.txt","r",encoding = 'utf8')
# coin = coin_txt.read()
# coin_txt.close()

# # 建立資料表
# command = '''CREATE TABLE if not exists '{}' (
# 	"cid"	 INTEGER NOT NULL,
# 	"open"	 INTEGER,
# 	"high"	 INTEGER,
# 	"low"	 INTEGER,
# 	"close"	 INTEGER,
# 	"volume" INTEGER,
#   "date"   TEXT ,
# 	PRIMARY KEY("cid" AUTOINCREMENT)
# );'''.format(coin)

# c.execute(command)


# crypto_price_data_list = get_candle_data()
# for i in range(len(crypto_price_data_list)):
#     open_price  = crypto_price_data_list[i]["open"]
#     high_price  = crypto_price_data_list[i]["high"]
#     low_price   = crypto_price_data_list[i]["low"]
#     close_price = crypto_price_data_list[i]["close"]
#     volume      = crypto_price_data_list[i]["volume"]
#     date_time   = str(millisecond2date(crypto_price_data_list[i]["period"]))
#     # print("open:"+open_price+" high:"+high_price+" low:"+low_price+" close:"+close_price+" volume:"+volume+" date:"+date_time)
#     insert_data = "insert into '{}'(open, high, low, close, volume, date) values('{}', '{}', '{}', '{}', '{}', '{}');".format(coin, open_price, high_price, low_price, close_price, volume, date_time)
#     c.execute(insert_data)


# conn.commit()