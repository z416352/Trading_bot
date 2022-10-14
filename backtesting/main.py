import sys
import os

cur_path =  os.path.abspath(os.path.dirname(__file__))
root_path = cur_path[:cur_path.find("Trading_bot\\")+len("Trading_bot\\")]
sys.path.append(root_path)
from Crawler.functions import *

import datetime as dt
import backtrader as bt
import backtrader.feeds as btfeeds
import math
import matplotlib as plt

# sma cross strategy
class SmaCross(bt.Strategy):
    # 交易紀錄
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    # 設定交易參數
    params = dict(
        ma_period_short=5,
        ma_period_long=10
    )

    def __init__(self):
        # 均線交叉策略
        sma1 = bt.ind.SMA(period=self.p.ma_period_short)
        sma2 = bt.ind.SMA(period=self.p.ma_period_long)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        
        # 使用自訂的sizer函數，將帳上的錢all-in
        self.setsizer(sizer())
        
        # 用開盤價做交易
        self.dataopen = self.datas[0].open

    def next(self):
        # 帳戶沒有部位
        if not self.position:
            # 5ma往上穿越20ma
            if self.crossover > 0:
                # 印出買賣日期與價位
                self.log('BUY ' + ', Price: ' + str(self.dataopen[0]))
                # 使用開盤價買入標的
                self.buy(price=self.dataopen[0])
        # 5ma往下穿越20ma
        elif self.crossover < 0:
            # 印出買賣日期與價位
            self.log('SELL ' + ', Price: ' + str(self.dataopen[0]))
            # 使用開盤價賣出標的
            self.close(price=self.dataopen[0])

# 計算交易部位
class sizer(bt.Sizer):
    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            return math.floor(cash/data[1])
        else:
            return self.broker.getposition(data)

if __name__ == '__main__':
    coin_txt = open("../Crawler/coin.txt","r",encoding = 'utf8')
    coin = coin_txt.read()
    coin_txt.close()

    DB = DB_table(db_name = "../Crawler/test.db", coin_name = coin)
    DB.init_db()

    df = DB.get_all()
    df.set_index('Timestamp', inplace=True)
    # print(df)

    cerebro = bt.Cerebro()
    data_bitcoin = bt.feeds.PandasData(dataname=df, fromdate=dt.datetime(2021,8,1), timeframe=bt.TimeFrame.Days)
    cerebro.adddata(data_bitcoin)
    # add strategy
    cerebro.addstrategy(SmaCross)
    # run backtest
    cerebro.run()
    # plot diagram
    cerebro.plot()