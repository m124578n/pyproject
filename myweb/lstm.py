# -*- coding: utf-8 -*-
"""
Created on Sun May 22 16:36:08 2022

@author: owo

"""

from pandas_datareader import data
import pandas as pd
import numpy as np
import talib
from talib import abstract
from sklearn.preprocessing import MinMaxScaler
from datetime import date,timedelta
from tensorflow.keras.models import load_model

def predicted(stock):
    XList=[stock]
    n_timestamp=60
    
    
    today_date=str(date.today())
    three_years_date=str(date.today() - timedelta(weeks=104))
    ta_list = ['DEMA']
    
    #股票預測資料=============================
    for x in XList:
        df = data.DataReader(x+".TW", "yahoo", three_years_date,today_date)
        Xdf=df[['Open','High','Low','Close','Volume']]
        Xdf.columns=['open','high','low','close','volume']
        
        #技術指標=============================
        for f in ta_list:
            try:
                output = eval('abstract.'+f+'(Xdf)')
                output.name = f.lower() if type(output) == pd.core.series.Series else None
                Xdf = pd.merge(Xdf, pd.DataFrame(output), left_on = Xdf.index, right_on = output.index)
                Xdf = Xdf.set_index('key_0')
            except:
                print(x,df.shape)
       
    Xdf=Xdf[Xdf['volume']!=0]
    Xdf['five_close']=(Xdf['close'].shift(-5))
    X_data=Xdf.iloc[-(5+n_timestamp):,3:]
    number=[]
    for i in range(len(X_data)):
        number.append(str(i-len(X_data)+6))
    
    
    #特徵標準化=============================
    mms  = MinMaxScaler(feature_range=(0, 1))
    X_data_sclaed=mms.fit_transform(X_data)
    
    #時間序列=============================
    def data_time_split(sequence,n_timestamp):
        X = []   
        for i in range(n_timestamp, len(sequence)):
            X.append(sequence[i-n_timestamp:i,:-1])
        return np.array(X)
    
    predicted_data = data_time_split(X_data_sclaed, n_timestamp)
    
    #載入模型=========================
    
    
    model = load_model(stock+'LSTM.h5')
    
    #預測=========================
    predicted_stock_price = model.predict(predicted_data)
    X_data_sclaed[-5:,3:]=np.around(predicted_stock_price,decimals=2)
    predicted_stock_price = mms.inverse_transform(X_data_sclaed)[:,3]
    predicted_stock_price.columns=['price']
    predicted_stock_price['number']=number
    
    return predicted_stock_price
#漲跌==========================
def stock_up_down(sequence):
    P=[]
    data=sequence[-6:]
    for i in range(5):
        if data[i+1]>data[i]:
            P.append('漲')
        else:
            P.append('跌')
    return P

# predicte_result=stock_up_down(predicted.predicted_stock_pricee)












