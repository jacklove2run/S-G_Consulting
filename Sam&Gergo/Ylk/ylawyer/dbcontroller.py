# -*- coding: utf-8 -*-
import json 
import datetime
from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict 
from ylawyer.models import ProductInfo, OrderList, UserInfo
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
##获取当前时间：
def current_datetime():
    now = datetime.datetime.now()
    return now
    
##查询失败反回错误码
def response_err_json():
    err_json = {'rtnCode' : 1, 'rtnMsg' : 'error'}
    return err_json
    #return HttpResponse(json.dumps(err_json), content_type="application/json")  

    
def response_no_product_err_json():
    err_json={'rtnCode' : 1, 'rtnMsg' : 'error: No this productId'}
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
def response_success_set_json(data):
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'success'}
    data_json = serializers.serialize("json", data, ensure_ascii=False)
    success_json['data'] = data_json
    return success_json

##获取用户信息
def getUserInfo(request, cur_user_id):
    try:
        userObj = UserInfo.objects.get(user_id=cur_user_id)       #################如果查询为空的时候是反回空json，还是反回错误？？
    except:
        err_json = response_err_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json") 
    else:
        success_json = response_success_json(userObj)
        return HttpResponse(json.dumps(success_json), content_type="application/json")      
    
##获取用户订单列表
def getOrderList(request,cur_user_id):
    try:
        order_list = OrderList.objects.filter(user_id=cur_user_id)
    except:
        err_json = response_err_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json")
    else：
        success_json = response_success_json(order_list)
        return HttpResponse(json.dumps(success_json), content_type="application/json")

##修改用户信息
def updateUserInfo(request):
    if request.method == 'POST':
        try:
            userObj = UserInfo.objects.get(user_id=request.POST['user_id'])
            userObj.name = request.POST['name']  #需考虑为中文时的情况
            userObj.phone = request.POST['phone']
            userObj.email = request.POST['email']
            userObj.address = request.POST['address']
            userObj.save()    
        except:
            resp_error = {'result' : 1}               #修改异常
            HttpResponse(json.dumps(resp_error), content_type="application/json")  
        else:    
            resp_success = {'result' : 0}             #修改成功
            HttpResponse(json.dumps(resp_success), content_type="application/json")

##新建用户订单
def insetUserOrderList(userId, productId):
    productObj = ProductInfo.objects.get(product_id=productId)
    if productObj == None:
        err_json = response_no_product_err_json()
        return HttpResponse(json.dumps(err_json), content_type="application/json")
    prod_dict_data = model_to_dict(productObj)  ##一个productId只对应一条记录
    cur_time = current_datetime()
    productName = prod_dict_data['product_name']
    productPrice = prod_dict_data['product_price']
    try:
        orderObj = OrderList(user_id=userId, product_name=productName, product_price=productPrice, time=cur_time)
        orderObj.save()
    except:
        err_json = response_err_json()
        return err_json
    else:
        success_json = success_json{'rtnCode' : 0, 'rtnMsg' : 'create order success'}
        return success_json
        
##新增收藏列表记录
def insetSavedProductList(userId, productId):
    try:
        savedProductObj = SavedProductList(user_id=userId,saved_product_id=productId)
        savedProductObj.save()
    except:
        err_json = response_err_json()
        return err_json
    else:
        success_json = success_json{'rtnCode' : 0, 'rtnMsg' : 'create saved product list success'}
        return success_json
##删除收藏列表记录
def deleteSavedProductList(userId, productId):
    try:
        SavedProductList.objects.filter(user_id=userId).delete()
    except:
        err_json = response_err_json()
        return err_json
    else:
        success_json = success_json{'rtnCode' : 0, 'rtnMsg' : 'delete saved product list success'}
        return success_json
##获取收藏列表
def getSavedProductList(request, cur_user_id):
    try:
        savedProductObj = SavedProductList.objects.filter(user_id=cur_user_id)     #################如果查询为空的时候是反回空json，还是反回错误？？
        savedProduct = savedProductObj.saved_product_id        ##多表查询
    except:
        response_err_json()
    else:
        response_success_json(savedProduct)
        


##购买/收藏/取消收藏商品操作        
def setProductState(request):
    if request.method == 'POST':
        try:
            productId = request.POST['product_id']
            userId = request.POST['user_id']
            typeId = request.POST['type']
        except:
            err_json = response_err_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            if productId == '' or userId == '' or typeId == '':
                err_json = {'rtnCode' : 1, 'rtnMsg' : 'Lack of necessary fileld like productId,userId,typeId'}
                return HttpResponse(json.dumps(err_json), content_type="application/json")
            if typeId == 1:        ##1. 购买 2. 收藏 3. 取消收藏
                rtnJson = insetUserOrderList(userId, productId)
                return HttpResponse(json.dumps(rtnJson), content_type="application/json")
            if typeId == 2:
                rtnJson = insetSavedProductList(userId, productId)
                return HttpResponse(json.dumps(rtnJson), content_type="application/json")
            if typeId == 3:
                rtnJson = deleteSavedProductList(userId, productId)
                return HttpResponse(json.dumps(rtnJson), content_type="application/json")
            else:
                err_json = {'rtnCode' : 1, 'rtnMsg' : 'wrong typeId'}
                return HttpResponse(json.dumps(err_json), content_type="application/json")
                