from pandas_datareader import data
from sklearn.ensemble  import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import math
import json
import joblib
import datetime


def ddd(num):
    data1=data.DataReader(str(num)+".TW","yahoo","1988-01-01")
    data1['y']=data1['Close'].shift(1)
    X=data1.loc['2020-01-01':,'High':'Adj Close']
    y=data1.loc['2020-01-01':,'y']
    reg=RandomForestRegressor()
    regmod=reg.fit(X, y)

    X=data1.loc[str(datetime.date.today() - datetime.timedelta(days=1)):str(datetime.date.today()),'High':'Adj Close']
    if len(X)==0:
        X=data1.loc[str(datetime.date.today() - datetime.timedelta(days=2)):str(datetime.date.today() - datetime.timedelta(days=1)),'High':'Adj Close']
        if len(X)==0:
            X=data1.loc[str(datetime.date.today() - datetime.timedelta(days=3)):str(datetime.date.today() - datetime.timedelta(days=2)),'High':'Adj Close']
    pr=regmod.predict(X)
    return pr


