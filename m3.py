#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import traceback
import time

from hbsdk import ApiClient, ApiError

API_KEY = "API_KEY"
API_SECRET = "API_SECRET"

client = ApiClient(API_KEY, API_SECRET)

def buildBuyOrders(buyAmount, buyPrice, sellPrice):
    return{
    'buyID' : None,
    'buyStatue': None,
    'buyPrice' : buyPrice,
    'buyAmount' : buyAmount,
    'buyedAmount' : 0,
    'sellPrice' : sellPrice,
    'sellPriceMin' : buyPrice*0.996004,
    'sellAmount' : 0,
    'selledAmount' : 0,
    'sellOrders' : [],
    }
# buyedAmount = sellAmount + selledAmount


def buildSellOrder(buyOrder):
    sellPrice = buyOrder['sellPrice']
    sellAmount = buyOrder['buyedAmount']
    sellOrder = {
        'sellID': None,
        'sellAmount': sellAmount,
        'selledAmount': 0,
    }
    buyOrder['buyedAmount'] -= sellAmount
    buyOrder['sellAmount'] += sellAmount
    buyOrder['sellOrders'].append(sellOrder)

def updateOrder(buyOrder):
    getBuyOrderInfo(buyOrder['buyID'])
    if xxx:
        buildSellOrder()
    for sellOrder in buyOrder['sellOrders']:
        getSellOrderInfo(sellOrder)
    


def executeOrder(coin, bidPrice, askPrice):
    order = coin['execOrder']
    if askPrice <= order['sellPriceMin']:
        print('---exit order---')
        coin['execOrder'] = None
    percent = round(0.996004*askPrice/bidPrice - 1, 4)
    print('---------------%s---------------'%coin['symbol'])
    print('%f %f %f'%(percent,bidPrice,askPrice))
    print coin['execOrder']
    
# coin
# bids: buy  price
# asks: sell price
def onDepth(coin, bids, asks):
    bidPrice,bidAmount = bids
    askPrice,askAmount = asks
    bidPrice += coin['minPrice']*2
    askPrice -= coin['minPrice']*2
    coin['percent'] = percent = round(0.996004*askPrice/bidPrice - 1, 4)
    if coin['execOrder'] is None:
        buyAmount = 20/bidPrice
        if percent > 0.001 and coin['execOrder'] is None:
            coin['execOrder'] = buildBuyOrders(buyAmount, bidPrice, askPrice)
            print('---------------%s---------------'%coin['symbol'])
            print('%f %f %f'%(percent,bidPrice,askPrice))
    else:
        executeOrder(coin, bidPrice, askPrice)

def coinType(x):
    return {
        'part' : x['symbol-partition'],
        'coin' : x['base-currency'],
        'money' : x['quote-currency'],
        'symbol' : x['base-currency'] + x['quote-currency'],
        'minPrice': 10**-x['price-precision'],
        'minAmount': 10**-x['amount-precision'],
        'percent': 0,
        'execOrder' : None,
    }

def getDepth(coin):
    while True:
        try:
            depth = client.mget('/market/depth', rkey='tick', symbol=coin['symbol'], type='step1')
            bids,asks = depth.bids[0],depth.asks[0]
            onDepth(coin, bids, asks)
            return coin
        except:
            print('------------EXCEPT------------')
            print coin['symbol']
            print(traceback.print_exc())
            print('------------======------------')
            time.sleep(1)

def main():
    allSymbol = client.mget('/v1/common/symbols')
    #coins = filter(lambda x:x['part'] == 'main' and x['money'] == 'usdt', map(coinType, allSymbol))
    coins = filter(lambda x:x['money'] == 'usdt', map(coinType, allSymbol))
    #coins = map(coinType, allSymbol)
    while True:
        print('**********************************************')
        coins = map(getDepth, coins)
        coins.sort(key=lambda x:x['percent'], reverse=True)
        time.sleep(1)

main()
