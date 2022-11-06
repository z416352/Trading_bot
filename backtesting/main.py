import sys
import os
import pathlib

sys.path.append(str(pathlib.Path().absolute())+"\..\DATA")
sys.path.append(str(pathlib.Path().absolute())+"\..\Crawler")
from functions import *

import datetime as dt
import backtrader as bt
import backtrader.feeds as btfeeds
import math
import matplotlib as plt

if __name__ == '__main__':
    coin_txt = open("../Crawler/coin.txt","r",encoding = 'utf8')
    coin = coin_txt.read()
    coin_txt.close()

    DB = DB_table(db_name = "../Crawler/test.db", coin_name = coin)
    DB.init_db()

    df = DB.get_all()
    df.set_index('Timestamp', inplace=True)
    print(df)
