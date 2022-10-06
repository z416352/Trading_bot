from functions import *

c, conn = init_db("test.db")

# coin_txt 放入要存入的幣別
coin_txt = open("coin.txt","r",encoding = 'utf8')
coin = coin_txt.read()
coin_txt.close()

create_table(c, coin)

crypto_df = get_candle_data()
# for i in range(len(crypto_price_data_list)):
#     open_price  = crypto_price_data_list[i]["open"]
#     high_price  = crypto_price_data_list[i]["high"]
#     low_price   = crypto_price_data_list[i]["low"]
#     close_price = crypto_price_data_list[i]["close"]
#     volume      = crypto_price_data_list[i]["volume"]
#     date_time   = str(millisecond2date(crypto_price_data_list[i]["period"]))
#     # print("open:"+open_price+" high:"+high_price+" low:"+low_price+" close:"+close_price+" volume:"+volume+" date:"+date_time)
#     insert_data(c, coin, open_price, high_price, low_price, close_price, volume, date_time)

# conn.commit()
