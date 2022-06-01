import email
from django.shortcuts import render,redirect
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from . import dddd
from .models import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pandas_datareader import data
from django.views.decorators.csrf import csrf_exempt
from prophet import Prophet
#from fbprophet import Prophet
import numpy as np
import pandas as pd
from datetime import date,timedelta
from pandas_datareader import data
import pandas as pd
import numpy as np
import talib
from talib import abstract
from sklearn.preprocessing import MinMaxScaler
from datetime import date,timedelta
from tensorflow.keras.models import load_model

# Create your views here.

def home(request):
    if request.POST:
        visitor = request.POST['Name']
        content = request.POST['Message']
        email = request.POST['Email']
        date_time = timezone.localtime(timezone.now()) # 擷取現在時間
        Commit.objects.create(visitor=visitor, email=email, content=content, datetime=date_time)
    return render(request ,'index.html',locals())
def login02(request):
    return render(request ,'login.html')
def signup(request):
    return render(request ,'signup.html')
# def test(request):
#     r=Test.objects.all()
#     if request.POST:
#        visitor = request.POST['visitor']
#        content = request.POST['content']
#        email = request.POST['email']
#        date_time = timezone.localtime(timezone.now()) # 擷取現在時間
#        Test.objects.create(visitor=visitor, email=email, content=content, date_time=date_time)
#     return render(request ,'test.html',locals())
@login_required(login_url="Login")
def prs1(request):
    ctx={
        'ddd_dd':"2603"
    }
    if request.POST:
        num=request.POST['a']
        try:
            data1=data.DataReader(str(num)+".TW","yahoo",'1977-01-01')
            data2=data1[['Open','Close','Low','High']]
            data2=data2.rename_axis('index').reset_index()
            data2['index']=data2['index'].astype(str)
            data2=data2.values.tolist()
            
            data3=data1.loc["2019-01-01":,:]
            data4 = pd.DataFrame(data3['Adj Close']).reset_index().rename(columns={'Date':'ds', 'Adj Close':'y'})
            model = Prophet()
            model.fit(data4)
            future = model.make_future_dataframe(periods=365) #forecasting for 1 year from now.
            forecast = model.predict(future)
            y1=list(forecast["yhat"])
            y2=list(forecast["yhat_upper"])
            y3=list(forecast["yhat_lower"])
            ds=list(forecast["ds"].astype(str))
            rd=list(data3['Adj Close'])
            
            ctx['pr']='fbprophet預測 {} 一年趨勢'.format(num)
            ctx['std']='股票代號 : {} 歷史資訊'.format(num)
            ctx['data2']=json.dumps(data2)
            ctx['y1']=json.dumps(y1)
            ctx['y2']=json.dumps(y2)
            ctx['y3']=json.dumps(y3)
            ctx['ds']=json.dumps(ds)
            ctx['rd']=json.dumps(rd)
        except:
            ctx['message']='無此股票代號或是系統忙碌請在重新輸入'
            return render(request ,'prs1.html',ctx)
    return render(request ,'prs1.html',ctx)

@login_required(login_url="Login")
def prs2(request):
    ctx={
        'ddd_dd':"2603"
    }
    if request.POST:
        num=request.POST['a']
        try:
            data1=data.DataReader(str(num)+".TW","yahoo",'1977-01-01')
            data2=data1[['Open','Close','Low','High']]
            data2=data2.rename_axis('index').reset_index()
            data2['index']=data2['index'].astype(str)
            data2=data2.values.tolist()
            pred=dddd.ddd(num)
            ctx['pr']='明日預測收盤價為={} 元'.format(round(pred[0],4))
            ctx['std']='股票代號 : {} 歷史資訊'.format(num)
            ctx['data2']=json.dumps(data2)
        except:
            ctx['message']='無此股票代號或是系統忙碌請在重新輸入'
            return render(request ,'prs2.html',ctx)

    return render(request ,'prs2.html',ctx)

@login_required(login_url="Login")
def prs3(request):
    ctx={
        'ddd_dd':"2603"
    }
    if request.POST:
        num=request.POST['a']
        try:
            data1=data.DataReader(str(num)+".TW","yahoo",'1977-01-01')
            data2=data1[['Open','Close','Low','High']]
            data2=data2.rename_axis('index').reset_index()
            data2['index']=data2['index'].astype(str)
            data2=data2.values.tolist()

            
            XList=[num]
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
            
            
            #model = load_model('/var/www/django/pyproject/myweb/'+str(num)+'LSTM.h5')
            model = load_model(str(num)+'LSTM.h5')

            #預測=========================
            predicted_stock_price = model.predict(predicted_data)
            X_data_sclaed[-5:,3:]=np.around(predicted_stock_price,decimals=2)
            predicted_stock_price = pd.DataFrame(mms.inverse_transform(X_data_sclaed)[:,3])
            predicted_stock_price.columns=['y']
            predicted_stock_price['ds']=number
            res=predicted_stock_price

            y1=list(res['y'])
            ds=list(res["ds"].astype(str))
            ctx['y1']=json.dumps(y1)
            ctx['ds']=json.dumps(ds)
            y=np.array(res['y'])
            y2=list(y[:-5])
            ctx['y2']=json.dumps(y2)
            ctx['pr1']='預測今天之後第一天的價格為 : {} 元'.format(round(y[-5],4))
            ctx['pr2']='預測今天之後第二天的價格為 : {} 元'.format(round(y[-4],4))
            ctx['pr3']='預測今天之後第三天的價格為 : {} 元'.format(round(y[-3],4))
            ctx['pr4']='預測今天之後第四天的價格為 : {} 元'.format(round(y[-2],4))
            ctx['pr5']='預測今天之後第五天的價格為 : {} 元'.format(round(y[-1],4))
            ctx['std']='股票代號 : {} 歷史資訊'.format(num)
            ctx['pr']='LSTM預測 {} 五天後股價'.format(num)
            ctx['data2']=json.dumps(data2)
        
            
            
            
            return render(request ,'prs3.html',ctx)
        except:
            ctx['message']='無此股票代號或是系統忙碌請在重新輸入'
            return render(request ,'prs3.html',ctx)
    return render(request ,'prs3.html',ctx)

@csrf_exempt
def register_view(request):

    form = RegisterForm()
    if request.method == "POST":
        form =  RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            return render(request, 'register.html', {'form':form,'message':'請依照指示輸入對應的格式，且帳號不得為中文．'})
    context = {
         'form': form
     }
    return render(request, 'register.html', context)

@login_required(login_url="Login")
def indexx(request):

    return render(request, 'indexx.html')
@csrf_exempt
def sign_in(request):
    form = LoginForm()
    if request.session.get('is_login', None):  # 不允許重複登入
        return redirect('/')
    if request.method == "POST":
        username = request.POST["account"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            request.session['is_login'] = True
            login(request, user)
            return redirect('/')  #重新導向到首頁
        else:
            return render(request, 'login.html', {'form':form,'message':'帳號或密碼錯誤！　新用戶'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('/login')

# def xxx(request):

#     expenses = Expense.objects.all()  # 查詢所有資料
#     form = ExpenseModelForm()
#     if request.method == "POST":
#         form = ExpenseModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect("/home/test")
#     context = {
#         'expenses': expenses,
#         'form': form
#     }
#     return render(request, 'test.html', context)

def update(request, pk):
    user = User.objects.get(id=pk)
    form = UpdateForm(instance=user)
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/indexx')
        else:
            context['message']='The password is too similar to the username.  This password is too short. It must contain at least 8 characters. This password is too common. This password is entirely numeric.'
            return render(request, 'update.html', context)
    
    return render(request, 'update.html', context)

# def delete(request, pk):
#     expense = Expense.objects.get(id=pk)
#     if request.method == "POST":
#         expense.delete()
#         return redirect('/home/test')
#     context = {
#         'expense': expense
#     }
#     return render(request, 'delete.html', context)

