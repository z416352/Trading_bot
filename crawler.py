import requests
from functions import *

crypto_price_data_list = get_candle_data()
for i in range(len(crypto_price_data_list)):
    print(crypto_price_data_list[i])

