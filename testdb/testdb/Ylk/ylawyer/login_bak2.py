#import base64
##根据wx.login()和wx.getUserInfo()传过来的encrypted_data, iv, code，获取session_key和openid
##生成一个168位的随机数当作3rd_session，把3rd_session当作key，session_key+openid当作value存到数据库
##把3rd_session传到客户端存储起来，下次登录校验3rd_session的时间是否过有效期
##如果过有效期，重新发起登录请求
##每次request要带上3rd_session，服务端进行3rd_session校验，根据3rd_session在数据库中查询，获取session_key和openid
##根据获取到的openid，在数据库中执行相关查询操作
import time
import os

#from dbcontroller import current_datetime
##encrypted_data, iv, 

from weixin import WXAPPAPI
from ylawyer.dbcontroller import current_datetime
import json 
import datetime
import pytz
from django import forms
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict 
from ylawyer.models import SessionOpenId



def get_login_session(request):                     ##从客户端传来的登录信息获取user info
    if request.method == 'POST':
        code = request.POST['code']
    #encryptedData = data['username']
    #iv = data['password']
    APP_ID = 'wx95f100449fab36b3'
    APP_SECRET = 'c0914c97100735c291193be50dbbebab'
    api = WXAPPAPI(appid=APP_ID,
                  app_secret=APP_SECRET)
    session_info = api.exchange_code_for_session_key(code=code)

# 获取session_info 后

    session_key = session_info.get('session_key')
    openid = session_info.get('openid')
    #crypt = WXBizDataCrypt(WXAPP_APPID, session_key)

# encrypted_data 包括敏感数据在内的完整用户信息的加密数据
# iv 加密算法的初始向量
# 这两个参数需要js获取
    #user_info = crypt.decrypt(encryptedData, iv)
    #openid = user_info.get('openId', None)
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'create order success', '3rd_session' : ''}
    if openid:
        trd_session = os.popen('head -n 80 /dev/urandom | tr -dc A-Za-z0-9 | head -c 168').read()   ##生成168位随机数当作key
        time = current_datetime()
        sessionObj = SessionOpenId(trd_session=trd_session,session_key=session_key, openId=openid, time=time)
        sessionObj.save()
    print(openid)
    print(session_key)
    success_json['3rd_session'] = trd_session
    return HttpResponse(json.dumps(success_json), content_type="application/json")  

        
        
##客户端方发起登录时根据客户端所传参数获取session_key和openid，并生成3rd_session,存储到数据库中并传3rd_session给客户端
def get_login_session_ver(encrypted_data, iv, code):
    user_info, session_key = get_wxapp_userinfo(encrypted_data, iv, code)
    openid = user_info.get('openId', None)
    if openid:
        trd_session = os.popen('head -n 80 /dev/urandom | tr -dc A-Za-z0-9 | head -c 168').read()   ##生成168位随机数当作key
        time = current_datetime()
        SessionOpenId(trd_session=trd_session,session_key=session_key, openId=openid, time=time)
    thdSession['3rd_session'] = trd_session
    return HttpResponse(json.dumps(thdSession), content_type="application/json")  
    
    
    

    
    
def verify_wxapp(encrypted_data, iv, code):
    user_info = get_wxapp_userinfo(encrypted_data, iv, code)
    openid = user_info.get('openId', None)
    if openid:
        auth = Account.get_by_wxapp(openid)
        if not auth:
            raise Unauthorized('wxapp_not_registered')
        return auth
    raise Unauthorized('invalid_wxapp_code')
