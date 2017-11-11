import datetime
import pytz
from django import forms
from django.forms.models import model_to_dict 
from ylawyer.models import SessionOpenId
from ylawyer import dbcontroller




##获取当前时间：
def current_datetime():
    #utc=pytz.UTC 
    timeZone = pytz.timezone('Asia/Shanghai')
    now = datetime.datetime.now()
    now = timeZone.localize(now)
    print(now)
    return now

##校验前端发起的查询所携带的用户加密过的trd_session
def check_session_value(trd_session):
    userId = dbcontroller.DEFAULT_INVALID_USERID
    try:
        trdSessionObj = SessionOpenId.objects.get(trd_session=trd_session)
        #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    except:
        return False, userId
    else:
        trdSessionList = model_to_dict(trdSessionObj)
        #print(trdSessionList)
        time = trdSessionList['time']
        #time = time.strftime('%b-%d-%y %H:%M:%S')
        cur_time = current_datetime()
        #print(time)
        #print(cur_time)
        #print((cur_time-time).days)
        if ((cur_time-time).days >= dbcontroller.SESSION_VALID_TIME_BY_DAYS):
            return False, userId
        userId = trdSessionList['user_id']
        return True, userId