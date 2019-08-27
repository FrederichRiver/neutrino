#!/usr/bin/python3

def get_technical_indicators(dataset):
    dataset['ma7'] = dataset['price'].rolling(window=7).mean()
    dataset['ma21'] = dataset['price'].rolling(window=21).mean()
    dataset['26ema'] = pd.ewma(dataset['price'], span=26)
    dataset['12ema'] = pd.ewma(dataset['price'], span=12)

    dataset['MACD'] = dataset['12ema'] -dataset['26ema']

    dataset['20sd'] = pd.stats.moments.rolling_std(dataset['price'], 20)
    dataset['upper_band'] = dataset['ma21'] + 2*dataset['20sd']
    dataset['lower_band'] = dataset['ma21'] - 2*dataset['20sd']
    dataset['ema'] = dataset['price'].ewm(com=0.5).mean()
    dataset['momentum'] = dataset['price'] - 1
    
    return dataset

def kdj():
    pass

def asi():
    pass

def boll():
    pass

def bara():
    pass

def wr():
    pass

def macd():
    pass

def nRSV(n:int):
    #cn = close price in n days
    #ln = lowest price in n days
    #hn = highest price in n days
    return 0.01*(cn-ln)/(hn-ln)

#
