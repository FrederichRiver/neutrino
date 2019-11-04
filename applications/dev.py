#!/usr/bin/python3
# from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pywt
from libmysql8 import mysqlHeader
from libstock import StockEventBase

__version__ = '1.0.2-beta'


# ARIMA
def arima_test():
    header = mysqlHeader('root', '6414939', 'test')
    event = StockEventBase()
    event._init_database(header)

    series = d['close']
    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit(disp=0)
    print(model_fit.summary())


def segment():
    import numpy as np
    import matplotlib.pyplot as plt

    header = mysqlHeader('root', '6414939', 'test')
    event = StockEventBase()
    event._init_database(header)

    stock_code = 'SH601818'
    sql = f"SELECT close_price from {stock_code}"
    result = event.mysql.engine.execute(sql).fetchall()
    seg = []
    for data in result:
        seg.append(data[0])
    seg = seg[:50]
    seg = np.array(seg)
    seg_fil = wavelet_nr(seg)
    plt.plot(seg)
    plt.plot(seg_fil)
    plt.show()


def wavelet_nr(df):
    """TODO: Docstring for wavelet_nr.

    :df: TODO
    :returns: TODO

    """
    db4 = pywt.Wavelet('db4')
    coeffs = pywt.wavedec(df, db4)
    coeffs[-1] *= 0
    coeffs[-2] *= 0
    meta = pywt.waverec(coeffs, db4)
    return meta
# FFT
# SHIBOR
# 26EMA
# BullingBand
# VIX
# SHANGHAI
# US Dollar
# Gold
# Metal
# Oil


if __name__ == "__main__":
    segment()
