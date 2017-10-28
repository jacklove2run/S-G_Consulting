# -*- coding: utf-8 -*-

import time
from django.http import HttpResponse
from ylawyer import config
#from ylawyer import wxpay
import sys
from wxpay import WxPay
#from wxpay import WxPay, get_nonce_str, dict_to_xml, xml_to_dict
import json 
import logging
import uuid
from api_pub import current_datetime, check_session_value
from ylawyer.dbcontroller import response_invalid_session_json, newOrderList
from ylawyer.models import ProductInfo, OrderList, UserInfo, SessionOpenId, SavedProductList, userAddrList

INVALID_TOTAL_FEE = 0

WRONG_PRODUCT_ID_INFO = {'rtnCode' : 2, 'rtnMsg' : 'Wrong Product id info!'}


def get_nonce_str():
    '''
    获取随机字符串
    :return:
    '''
    return str(uuid.uuid4()).replace('-', '')
    

def create_first_pay_data(openid, total_fee):
    data = {
                'appid': config.appid,
                'mch_id': config.mch_id,
                'nonce_str': get_nonce_str(),
                'body': 'aa',                              # 商品描述
                'out_trade_no': str(int(time.time())),       # 商户订单号
                'total_fee': total_fee,
                'spbill_create_ip': config.spbill_create_ip,
                'notify_url': config.notify_url,
                'attach': '{"msg": "tesst message"}',
                'trade_type': config.trade_type,
                'openid': openid
            }
    return data
    
def getTotalFeeByProductList(productIdList):
    total_fee = 0
    try:
        for productId in productIdList:
            ProductInfoObj = ProductInfo.objects.get(product_id=productId)
            total_fee += ProductInfoObj.product_price * 100
    except:
        return INVALID_TOTAL_FEE
    else:
        return total_fee

        
        
def getproductIdListFromStr(productIdListStr):
    productIdList = []
    if productIdListStr == '':
        return productIdList
    productId = ''
    for str in productIdListStr:
        if str != '&':
            productId += str
        else:
            productIdList.append(productId)
            productId = ''
    if productId != '':
        productIdList.append(productId)
    return productIdList
def create_pay(request):
    '''
    请求支付
    :return:
    '''
    if request.method == 'POST':
        trd_session = request.POST['trd_session']
        productIdListStr = request.POST['productIdListStr']
        productIdList = getproductIdListFromStr(productIdListStr)
        print(productIdList)
        total_fee = getTotalFeeByProductList(productIdList)
        if total_fee == INVALID_TOTAL_FEE:
            return HttpResponse(WRONG_PRODUCT_ID_INFO, content_type="application/json")
        isFirstOrder = request.POST['isFirstOrder'] ##0表示不是第一次下单，1表示第一次下单
        print(isFirstOrder)
        isValidSession, curUserId= check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            SessionOpenIdObj = SessionOpenId.objects.get(user_id=curUserId)
            openid = SessionOpenIdObj.openId
            if isFirstOrder == 'True':
                print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                data = create_first_pay_data(openid, total_fee)
                out_trade_no = data['out_trade_no']
            else:
                out_trade_no = request.POST['out_trade_no'] #订单号
                data = create_first_pay_data(openid, total_fee)
                data['out_trade_no'] = out_trade_no
            err_json = {'rtnCode' : 1, 'rtnMsg' : 'pay error'}
            wxpay = WxPay(config.merchant_key, **data)
            pay_info = wxpay.get_pay_info() 
            #pay_info_json = json.dumps(pay_info)
            #print(pay_info)
            sign = pay_info['sign']
            pay_info.pop('sign')
            pay_info['total_fee'] =  total_fee
            pay_info['rtnCode'] = 1
            pay_info['rtnMsg'] = 'wxpay request success!'
            print(pay_info)
            if pay_info:
                if isFirstOrder == 'True':
                    newOrderList(curUserId, productIdList, out_trade_no, sign)
                return HttpResponse(json.dumps(pay_info), content_type="application/json")
            return HttpResponse(json.dumps(err_json), content_type="application/json")
    
    
def wxpay(request):
    '''
    支付回调通知
    :return:
    '''
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    if request.method == 'POST':
        try:
            data = xml_to_dict(request.data)
            result_code = data['result_code']
            sign = data['sign']
            total_fee = data['total_fee']
            openid = data['openid']
            out_trade_no = data['out_trade_no']
            orderListObj = OrderList.objects.get(out_trade_no=out_trade_no)
        except Exception as e:
            logging.error(e)
        else:
            print(data)
            if result_code == 'SUCESS' and total_fee == orderListObj:
                orderListObj.order_status = DEFAULT_ORDER_SAVED_STATUS
                orderListObj.save()
        result_data = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }
        return HttpResponse(dict_to_xml(result_data), content_type="application/xml")
        #return dict_to_xml(result_data), {'Content-Type': 'application/xml'}