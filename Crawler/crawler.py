from functions import *
import pandas as pd

# get from https://www.finlab.tw/btc-crawler-py/
from crypto_backtrader.finlab import crypto


# coin_txt 放入要存入的幣別
coin_txt = open("coin.txt","r",encoding = 'utf8')
coin = coin_txt.read()
coin_txt.close()

DB = DB_table(db_name = "test.db", coin_name = coin)

DB.init_db()

DB.update(interval='h1')

# DB.show()
