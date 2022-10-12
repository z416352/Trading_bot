from functions import *
import pandas as pd

c, conn = init_db("test.db")

# coin_txt 放入要存入的幣別
coin_txt = open("coin.txt","r",encoding = 'utf8')
coin = coin_txt.read()
coin_txt.close()

# create_table(c, coin)

update_table(conn, coin)

df = show_all_data(conn, coin)
print(df)