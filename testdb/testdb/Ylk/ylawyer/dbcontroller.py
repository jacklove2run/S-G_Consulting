# -*- coding: utf-8 -*-
import json 
import datetime
import pytz
from django import forms
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict 
from ylawyer.models import ProductInfo, OrderList, UserInfo, SessionOpenId, SavedProductList, userAddrList
from api_pub import current_datetime, check_session_value
from product_list import PRODUCT_LIST
import logging
#/order/get_order_list       //获取用户订单
'''
params: {
    product_id:                //把每个商品都编号
}
response: {
    rtnCode: 0,
    rtnMsg: 'ok',
    data: {
        id: 
        name:
        type: 1            // 商品状态， 0；不可购买 1: 可购买
        saved_state: 0      //商品收藏状态：0:未收藏 1：已收藏     默认未收藏
        images: []
        messages: []
    }
}
'''
DEFAULT_INVALID_USERID = 0
DEFAULT_ORDER_SAVED_STATUS = 0     ##订单已支付
DEFAULT_ORDER_UNSAVED_STATUS = 1   ##默认订单为未支付

SESSION_VALID_TIME_BY_SECONDS = 30 * 24 * 3600
SESSION_VALID_TIME_BY_DAYS = 30
UPDATE_OUT_TRADE_NO_FAIL_JSON = {'rtnCode' : 2, 'rtnMsg' : 'update out trade NO. failed'}
UPDATE_OUT_TRADE_NO_SUCCESS_JSON = {'rtnCode' : 0, 'rtnMsg' : 'update out trade NO. success'}
def get_all_product_list_success_json():
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'get all product list info success', 'data' : ''}
    
    success_json['data'] = PRODUCT_LIST
    return success_json






##查询成功的空json
def success_none_json():
    success_none_json_data = {'rtnCode' : 0, 'rtnMsg' : 'no saved product in the list', 'data' : ''}
    return success_none_json_data



 

##用户session检查失败错误码
def response_invalid_session_json():
    err_json = {'rtnCode' : 1, 'rtnMsg' : 'invalid session! please login again'}
    return err_json

    
##查询失败反回错误码
def response_err_json():
    err_json = {'rtnCode' : 2, 'rtnMsg' : 'error'}
    return err_json
    #return HttpResponse(json.dumps(err_json), content_type="application/json")  

def response_no_user_json():
    err_json = {'rtnCode' : 0, 'rtnMsg' : 'no this user info'}
    return err_json
    #return HttpResponse(json.dumps(err_json), content_type="application/json") 
    
def response_no_product_err_json():
    err_json={'rtnCode' : 3, 'rtnMsg' : 'error: No this productId'}
    return err_json
    

##查询成功返回成功码和data
def response_success_json(data):
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'success'}
    dict_data = model_to_dict(data)  ##将查询结果集转换成字典      注：此处有问题，model_to_dict只能转换单个对象，对于结果集则无法转换。
    success_json['data'] = dict_data  ##在反回的json中添加查询结果data         
    #dict_data.update(success_json)   ##将查询结果集与反回码合并成一个json
    return success_json
    #return HttpResponse(json.dumps(dict_data), content_type="application/json")  
    

##序列化查询结果集为json格式
def response_success_order_set_json(data):
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'success'}
    dataList = []
    if data != None:
        for cur_data in data:
            id = cur_data.product_id
            userId = cur_data.user_id
            productName = cur_data.product_name.encode('utf-8').decode('utf-8')
            print(cur_data.product_name)
            productPrice = cur_data.product_price
            #time = cur_data.time.strftime('%b-%d-%y %H:%M:%S')
            time = cur_data.time.strftime('%Y/%m/%d %H:%M:%S')
            productDesc = cur_data.product_desc
            imgUrl = cur_data.img_url
            out_trade_no = cur_data.out_trade_no
            out_trade_show_no = cur_data.out_trade_show_no
            orderInfo = dict()
            orderInfo.update(id=id, user_id=userId, product_name=productName, product_desc=productDesc, product_price=productPrice, time=time, img_url=imgUrl, out_trade_no=out_trade_no, out_trade_show_no=out_trade_show_no)
            #print(orderInfo)
            dataList.append(orderInfo)
        success_json['data'] = dataList
        return success_json
        
####序列化查询结果集为json格式
def response_success_addr_set_json(data):
    success_json = {
        'rtnCode' : 0, 
        'rtnMsg' : 'Get address success!'             
    }
    dataList = []
    for cur_data in data:
        recv_name = cur_data.recipient_name
        recv_phone = cur_data.recipient_phone
        recv_addr = cur_data.recipient_addr
        addr_id = cur_data.addr_id
        addrDict = dict()
        addrDict.update(recv_name=recv_name, recv_phone=recv_phone, recv_addr=recv_addr, addr_id=addr_id)
        dataList.append(addrDict)
    success_json['data'] = dataList
    return success_json
        
        

        
##获取保存的产品列表
def resp_success_saved_product_set_json(data):
    error_json = {'rtnCode' : 2, 'rtnMsg' : 'error'}
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'success'}
    dataList = []
    for cur_data in data:
        try:
            productObj = ProductInfo.objects.get(product_id=cur_data.saved_product_id)
            #productObj.
        except:
            return error_json
        else:
            product_id = productObj.product_id
            product_name = productObj.product_name
            product_price = productObj.product_price
            product_desc = productObj.product_desc
            product_img_url = productObj.product_img_url
            
            product_address = productObj.product_address
            service_type = productObj.service_type
            service_address = productObj.service_address
            service_way = productObj.service_way
            service_time = productObj.service_time 
            
            productDict = dict()
            productDict.update(product_id=product_id, product_name=product_name, product_price=product_price, product_desc=product_desc, product_img_url=product_img_url, product_address=product_address, service_type=service_type, service_address=service_address, service_way=service_way, service_time=service_time)
            
            dataList.append(productDict)
            success_json['data'] = dataList   
    return success_json
            
##获取地址列表         
def getRecvOrderAddr(request, trd_session):
    isValidSession, curUserId= check_session_value(trd_session)
    if isValidSession == False:
        err_json = response_invalid_session_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json")
    else:
        userAddrObj = userAddrList.objects.filter(user_id=curUserId)
        if userAddrObj.exists():
            success_json = response_success_addr_set_json(userAddrObj)
            return HttpResponse(json.dumps(success_json), content_type="application/json")
        else:
            non_json = {'rtnCode' : 0, 'rtnMsg' : 'no data in addr list'}
            return HttpResponse(json.dumps(non_json), content_type="application/json")
            
##删除地址
def deleteRecvOrderAddr(request):
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'Delete user address success!'}
    if request.method == 'POST':
        trd_session = request.POST['trd_session']
        isValidSession, curUserId= check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            try:
                addressId = request.POST['addr_id']
                userAddrList.objects.filter(addr_id=addressId).delete()
            except:
                err_json = response_err_json()
                return HttpResponse(json.dumps(err_json), content_type="application/json")
            else:
                return HttpResponse(json.dumps(success_json), content_type="application/json")
    
            
##新增我的地址
def addRecvOrderAddr(request):
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'Add new user address success!', 'addr_id' : ''}
    err_resp_json = {'rtnCode' : 2, 'rtnMsg' : 'Add new user address failed! please check', 'addr_id' : ''}
    if request.method == 'POST':
        trd_session = request.POST['trd_session']
        isValidSession, curUserId= check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            recvName = request.POST['recv_name']
            recvPhone = request.POST['recv_phone']
            recvAddr = request.POST['recv_addr']
            userAddrObj = userAddrList(user_id=curUserId, recipient_name=recvName, recipient_phone=recvPhone, recipient_addr=recvAddr)
            userAddrObj.save()
            try:
                userAddObjAft = userAddrList.objects.get(user_id=curUserId, recipient_name=recvName, recipient_phone=recvPhone, recipient_addr=recvAddr)
            except:
                return HttpResponse(json.dumps(err_resp_json), content_type="application/json")
            else:
                addr_id = userAddObjAft.addr_id
                success_json['addr_id'] = addr_id
                return HttpResponse(json.dumps(success_json), content_type="application/json")
##设置我的地址
def setRecOrderAddr(request):
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'Set new user address success!', 'addr_id' : 0}
    if request.method == 'POST':
        trd_session = request.POST['trd_session']
        isValidSession, curUserId= check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            addressId = request.POST['addr_id']
            recvName = request.POST['recv_name']
            recvPhone = request.POST['recv_phone']
            recvAddr = request.POST['recv_addr']
            try:
                userAddObjAft = userAddrList.objects.get(addr_id=addressId)
            except:
                err_resp_json = {'rtnCode' : 2, 'rtnMsg' : 'Update user address failed! please check'}
                return HttpResponse(json.dumps(err_resp_json), content_type="application/json")
            else:
                userAddObjAft.recipient_name = recvName
                userAddObjAft.recipient_phone = recvPhone
                userAddObjAft.recipient_addr = recvAddr
                userAddObjAft.save()
                success_json['addr_id'] = addressId
                print(recvAddr)
                return HttpResponse(json.dumps(success_json), content_type="application/json")
        
##获取        
            
#获取首页产品列表，按照导航栏标签区分：
def getAllProductList(request):
    success_json = get_all_product_list_success_json()
    return HttpResponse(json.dumps(success_json), content_type="application/json")


            
##根据用户信息和产品id获取产品的收藏状态
def getProductStoredInfo(request, cur_product_id, trd_session):
    error_json = {'rtnCode' : 0, 'rtnMsg' : 'success', 'status' : '1'}     #1表示未收藏
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'success', 'status' : '0'}   #0表示收藏
    isValidSession, curUserId= check_session_value(trd_session)
    if isValidSession == False:
        err_json = response_invalid_session_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json")
    else:
        print(curUserId)
        print(cur_product_id)
        savedProductObj = SavedProductList.objects.filter(user_id=curUserId, saved_product_id=cur_product_id)
        print(savedProductObj.exists())
        if savedProductObj.exists():
            return HttpResponse(json.dumps(success_json), content_type="application/json")
        else:
            return HttpResponse(json.dumps(error_json), content_type="application/json")
            
            
#获取产品详细信息
def getProductInfo(request, cur_product_id):
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'success'}
    error_json = {'rtnCode' : 2, 'rtnMsg' : 'Wrong Product Id'}
    dataList = []
    try:
        productObj = ProductInfo.objects.get(product_id=cur_product_id)
    except:
        return HttpResponse(json.dumps(error_json), content_type="application/json")
    else:
        product_id = productObj.product_id
        product_name = productObj.product_name
        product_price = productObj.product_price
        product_desc = productObj.product_desc
        product_img_url = productObj.product_img_url
        
        product_address = productObj.product_address
        service_type = productObj.service_type
        service_address = productObj.service_address
        service_way = productObj.service_way
        service_time = productObj.service_time 
        
        productDict = dict()
        productDict.update(product_id=product_id, product_name=product_name, product_price=product_price, product_desc=product_desc, product_img_url=product_img_url, product_address=product_address, service_type=service_type, service_address=service_address, service_way=service_way, service_time=service_time)
        
        dataList.append(productDict)
        success_json['data'] = dataList
        return HttpResponse(json.dumps(success_json), content_type="application/json")
        
        
        
    
##获取用户信息
def getUserInfo(request, trd_session):
    try:
        isValidSession, curUserId= check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else: 
            userObj = UserInfo.objects.get(user_id=curUserId)
    except:
        err_json = response_no_user_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json") 
    else:
        success_json = response_success_json(userObj)
        return HttpResponse(json.dumps(success_json), content_type="application/json")     


    
##获取用户已完成订单列表
def getOrderList(request,trd_session):
    isValidSession, curUserId= check_session_value(trd_session)
    print(isValidSession)
    if isValidSession == False:
        err_json = response_invalid_session_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json")
    else:   
        order_list = OrderList.objects.filter(user_id=curUserId, order_status=DEFAULT_ORDER_SAVED_STATUS)
    success_json = response_success_order_set_json(order_list)
    print(success_json)
    return HttpResponse(json.dumps(success_json), content_type="application/json")

##获取用户未完成订单列表
def getUnsavedOrderList(request,trd_session):
    isValidSession, curUserId= check_session_value(trd_session)
    if isValidSession == False:
        err_json = response_invalid_session_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json")
    else:   
        order_list = OrderList.objects.filter(user_id=curUserId, order_status=DEFAULT_ORDER_UNSAVED_STATUS)
    #except:
    #    err_json = response_err_json()
    #    return HttpResponse(json.dumps(err_json), content_type="application/json")
    #else:
    success_json = response_success_order_set_json(order_list)
    return HttpResponse(json.dumps(success_json), content_type="application/json")
        


##修改用户信息
def updateUserInfo(request):
    print(request.method)
    err_resp_json = {'rtnCode' : 0, 'rtnMsg' : 'create userObj success'}
    if request.method == 'POST':
        #try:
        trd_session = request.POST['trd_session']
        isValidSession, curUserId= check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            try:
                userObj = UserInfo.objects.get(user_id=curUserId)
            except:
                userObj = UserInfo(user_id=curUserId, name=request.POST['name'], phone=request.POST['phone'], email=request.POST['email'])
                userObj.save()
                return HttpResponse(json.dumps(err_resp_json), content_type="application/json")
            else:
                userObj.name = request.POST['name']  #需考虑为中文时的情况
                userObj.phone = request.POST['phone']
                userObj.email = request.POST['email']
                #userObj.address = request.POST['address']
                userObj.save()
                resp_success = {'rtnCode' : 0, 'rtnMsg' : 'update userObj success'}             #修改成功
                return HttpResponse(json.dumps(resp_success), content_type="application/json")

##新建已成功支付订单
def insetUserOrderList(userId, productId):
    try:
        productObj = ProductInfo.objects.get(product_id=productId)
       
    except:
        err_json = response_no_product_err_json()
        return err_json
    else:
        prod_dict_data = model_to_dict(productObj)  ##一个productId只对应一条记录
        cur_time = current_datetime()
        productName = prod_dict_data['product_name']
        productDesc = prod_dict_data['product_desc']
        productPrice = prod_dict_data['product_price']
        orderStatus = DEFAULT_ORDER_SAVED_STATUS
        imgUrl = prod_dict_data['product_img_url']
        
        orderObj = OrderList(user_id=userId, product_name=productName, product_price=productPrice, product_desc=productDesc, order_status= orderStatus, img_url=imgUrl, time=cur_time)
        orderObj.save()
        success_json = {'rtnCode' : 0, 'rtnMsg' : 'create order success'}
        return success_json
        
def delUnPaidOrder(request):
    if request.method == 'POST':
        out_trade_show_no = request.POST['out_trade_show_no']
        trd_session = request.POST['trd_session']
        isValidSession, curUserId = check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            try:
                OrderListObj = OrderList.objects.filter(user_id=curUserId, out_trade_show_no=out_trade_show_no, order_status=DEFAULT_ORDER_UNSAVED_STATUS).delete()
            except:
                err_json = {'rtnCode' : '2', 'rtnMsg' : 'wrong out_trade_no!'}
                return HttpResponse(json.dumps(err_json), content_type="application/json")
            else:
                success_json = {'rtnCode' : 0, 'rtnMsg' : 'delete order success'}   
                return HttpResponse(json.dumps(success_json), content_type="application/json")                
##新建未支付订单
def insetUnPaidOrderList(userId, productId):
    try:
        productObj = ProductInfo.objects.get(product_id=productId)
       
    except:
        err_json = response_no_product_err_json()
        return err_json
    else:
        prod_dict_data = model_to_dict(productObj)  ##一个productId只对应一条记录
        cur_time = current_datetime()
        productName = prod_dict_data['product_name']
        productDesc = prod_dict_data['product_desc']
        productPrice = prod_dict_data['product_price']
        orderStatus = DEFAULT_ORDER_UNSAVED_STATUS
        imgUrl = prod_dict_data['product_img_url']
        
        orderObj = OrderList(user_id=userId, product_name=productName, product_price=productPrice, product_desc=productDesc, order_status= orderStatus, img_url=imgUrl, time=cur_time)
        orderObj.save()
        success_json = {'rtnCode' : 0, 'rtnMsg' : 'create order success'}
        return success_json
 
##统一下单  


def newOrderList(curUserId, productList, out_trade_show_no, out_trade_no, sign, addrId):
    for productId in productList:
        resp_json = newOrder(curUserId, productId, out_trade_show_no, out_trade_no, sign, addrId)
        if resp_json['rtnCode'] != 0:
            return resp_json
    return resp_json
    
##更新订单的微信校验订单号
def updateOrderListOutTradeNoByOutTradeShowNoList(out_trade_no, outTradeShowNoList):
    try:
        for outTradeShowNo in outTradeShowNoList:
            orderListObj = OrderList.objects.get(out_trade_show_no=outTradeShowNo)
            orderListObj.out_trade_no = out_trade_no
            orderListObj.save()
    except Exception as e:
        logging.error(e)
        return UPDATE_OUT_TRADE_NO_FAIL_JSON
    else:
        return UPDATE_OUT_TRADE_NO_SUCCESS_JSON
    
        
##统一下单，新建未支付订单
def newOrder(curUserId, productId, out_trade_show_no, out_trade_no, sign, addrId):
    try:
        productObj = ProductInfo.objects.get(product_id=productId)
    except:
        err_json = response_no_product_err_json()
        return err_json
    else:
        prod_dict_data = model_to_dict(productObj)  ##一个productId只对应一条记录
        cur_time = current_datetime()
        productName = prod_dict_data['product_name']
        productDesc = prod_dict_data['product_desc']
        productPrice = prod_dict_data['product_price']
        orderStatus = DEFAULT_ORDER_UNSAVED_STATUS
        imgUrl = prod_dict_data['product_img_url']
        
        orderObj = OrderList(user_id=curUserId, product_name=productName, product_price=productPrice, product_desc=productDesc, order_status= orderStatus, img_url=imgUrl, time=cur_time, out_trade_no=out_trade_no, sign=sign, addr_id=addrId, out_trade_show_no=out_trade_show_no, product_id=productId)
        orderObj.save()
        success_json = {'rtnCode' : 0, 'rtnMsg' : 'create order success'}
        return success_json
        
        
##新增收藏列表记录
def insetSavedProductList(userId, productId):
    try:
        savedProductObj = SavedProductList.objects.filter(user_id=userId, saved_product_id=productId)
        if savedProductObj.exists():
            success_json = {'rtnCode' : 0, 'rtnMsg' : 'the product is already in the saved productList'}
            return success_json
        savedProductObj = SavedProductList(user_id=userId,saved_product_id=productId)
        savedProductObj.save()
    except:
        err_json = response_err_json()
        return err_json
    else:
        success_json = {'rtnCode' : 0, 'rtnMsg' : 'create saved product list success'}
        return success_json
##删除收藏列表记录
def deleteSavedProductList(userId, productId):
    try:
        SavedProductList.objects.filter(user_id=userId, saved_product_id=productId).delete()
    except:
        err_json = response_err_json()
        return err_json
    else:
        success_json = {'rtnCode' : 0, 'rtnMsg' : 'delete saved product list success'}
        return success_json
##获取收藏列表
def getSavedProductList(request, trd_session):
    isValidSession, curUserId= check_session_value(trd_session)
    if isValidSession == False:
        err_json = response_invalid_session_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json")
    else:
        savedProductObj = SavedProductList.objects.filter(user_id=curUserId)     #################如果查询为空的时候是反回空json，还是反回错误？？
        if savedProductObj.exists():
            resp_json = resp_success_saved_product_set_json(savedProductObj)
            return HttpResponse(json.dumps(resp_json), content_type="application/json")
        else:
            resp_json = success_none_json()
            return HttpResponse(json.dumps(resp_json), content_type="application/json")


##购买/收藏/取消收藏商品操作        
def setProductState(request):
    if request.method == 'POST':
        try:
            trd_session = request.POST['trd_session']
            productId = request.POST['product_id']
            typeId = request.POST['type']
            isValidSession, curUserId= check_session_value(trd_session)
            if isValidSession == False:
                err_json = response_invalid_session_json()
                return HttpResponse(json.dumps(err_json), content_type="application/json")
        except:
            err_json = response_err_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            if productId == '' or trd_session == '' or typeId == '':
                err_json = {'rtnCode' : 2, 'rtnMsg' : 'Lack of necessary fileld like productId,userId,typeId'}
                return HttpResponse(json.dumps(err_json), content_type="application/json")
                print(typeId)
            if typeId == '1':        ##1. 购买成功 2. 收藏 3. 取消收藏 4. 购买未成功
                rtnJson = insetUserOrderList(curUserId, productId)
                return HttpResponse(json.dumps(rtnJson), content_type="application/json")
            if typeId == '2':
                rtnJson = insetSavedProductList(curUserId, productId)
                return HttpResponse(json.dumps(rtnJson), content_type="application/json")
            if typeId == '3':
                rtnJson = deleteSavedProductList(curUserId, productId)
                return HttpResponse(json.dumps(rtnJson), content_type="application/json")
            if typeId == '4':
                rtnJson = insetUnPaidOrderList(curUserId, productId)
                return HttpResponse(json.dumps(rtnJson), content_type="application/json")
            else:
                err_json = {'rtnCode' : 1, 'rtnMsg' : 'wrong typeId'}
                return HttpResponse(json.dumps(err_json), content_type="application/json")
                
                
                

                
