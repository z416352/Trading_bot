from functions import *
import pandas as pd

# get from https://www.finlab.tw/btc-crawler-py/
from crypto_backtrader.finlab import crypto

# coin_txt 放入要存入的幣別
coin_txt = open("../DATA/coin.txt","r",encoding = 'utf8')
coin = coin_txt.read()
coin_txt.close()

DB = DB_table(db_file_path="../DATA/test.db", coin_name=coin)

DB.init_db()
DB.create()
DB.update(Interval='8h')

print(DB.get_all())