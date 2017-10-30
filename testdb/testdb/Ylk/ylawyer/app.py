# -*- coding: utf-8 -*-

import os
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
from ylawyer.dbcontroller import response_invalid_session_json, newOrderList, updateOrderListOutTradeNoByOutTradeShowNoList
from ylawyer.models import ProductInfo, OrderList, UserInfo, SessionOpenId, SavedProductList, userAddrList

INVALID_TOTAL_FEE = 0

WRONG_PRODUCT_ID_INFO = {'rtnCode' : 2, 'rtnMsg' : 'Wrong Product id or out_trade_no info!'}
DEFAULT_ORDER_ADDR_ID = 0
DEFAULT_OUT_TRADE_NO = '9999999999'
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
                'out_trade_no': '',       # 商户订单号
                'total_fee': total_fee,
                'spbill_create_ip': config.spbill_create_ip,
                'notify_url': config.notify_url,
                'attach': '{"msg": "tesst message"}',
                'trade_type': config.trade_type,
                'openid': openid,
                'timeStamp' : str(int(time.time()))
            }
    out_trade_show_no = str(int(time.time()))
    data['out_trade_no'] = out_trade_show_no + os.popen('head -n 80 /dev/urandom | tr -dc a-z0-9 | head -c 10').read()
    return data, out_trade_show_no
    
def getTotalFeeByProductList(productIdList):
    total_fee = 0
    try:
        for productId in productIdList:
            ProductInfoObj = ProductInfo.objects.get(product_id=productId)
            total_fee += int(ProductInfoObj.product_price * 100)
    except:
        return INVALID_TOTAL_FEE
    else:
        return total_fee

def getTotalFeeByOutTradeShowNoList(outTradeShowNoList):
    total_fee = 0
    try:
        for outTradeShowNo in outTradeShowNoList:
            orderListObj = OrderList.objects.get(out_trade_show_no=outTradeShowNo)
            total_fee += int(orderListObj.product_price * 100)
    except:
        return INVALID_TOTAL_FEE
    else:
        return total_fee
        
def getOutTradeShowNoListFromStr(outTradeShowNoListStr):
    outTradeShowNoList = []
    if outTradeShowNoListStr == '':
        return productIdList
    outTradeShowNo = ''
    for str in outTradeShowNoListStr:
        if str != '&':
            outTradeShowNo += str
        else:
            outTradeShowNoList.append(outTradeShowNo)
            outTradeShowNo = ''
    if outTradeShowNo != '':
        outTradeShowNoList.append(outTradeShowNo)
    return outTradeShowNoList
def create_pay(request):
    '''
    请求支付
    :return:
    '''
    if request.method == 'POST':
        trd_session = request.POST['trd_session']
        isValidSession, curUserId= check_session_value(trd_session)
        if isValidSession == False:
            err_json = response_invalid_session_json()
            return HttpResponse(json.dumps(err_json), content_type="application/json")
        else:
            isFirstOrder = request.POST['isFirstOrder'] ##0表示不是第一次下单，1表示第一次下单
            if isFirstOrder == '1':
                productId = request.POST['product_id']
                if 'addr_id' in request.POST:            ##表示点击直接购买
                    addrId = request.POST['addr_id']
                else:
                    addrId = DEFAULT_ORDER_ADDR_ID      ##表示点击加入购物车
                productList = []
                productList.append(productId)
                total_fee = getTotalFeeByProductList(productList)
            else:
                outTradeShowNoListStr = request.POST['outTradeShowNoListStr']
                outTradeShowNoList = getOutTradeShowNoListFromStr(outTradeShowNoListStr)
                total_fee = getTotalFeeByOutTradeShowNoList(outTradeShowNoList)
                addrId = request.POST['addr_id']
                print(outTradeShowNoList)
            print(total_fee)
            if total_fee == INVALID_TOTAL_FEE:
                return HttpResponse(WRONG_PRODUCT_ID_INFO, content_type="application/json")
            SessionOpenIdObj = SessionOpenId.objects.get(user_id=curUserId)
            openid = SessionOpenIdObj.openId
            if isFirstOrder == '1':
                data, out_trade_show_no = create_first_pay_data(openid, total_fee)
            else:
                data, out_trade_show_no = create_first_pay_data(openid, total_fee)
                #data['out_trade_no'] = out_trade_no
            out_trade_no = data['out_trade_no']
            err_json = {'rtnCode' : 2, 'rtnMsg' : 'pay error'}
            wxpay = WxPay(config.merchant_key, **data)
            pay_info = wxpay.get_pay_info() 
            #pay_info_json = json.dumps(pay_info)
            #print(pay_info)
            sign = pay_info['sign']
            pay_info.pop('sign')
            #pay_info['total_fee'] =  total_fee
            pay_info['rtnCode'] = 0
            pay_info['rtnMsg'] = 'wxpay request success!'
            #print(pay_info)
            if pay_info:
                if isFirstOrder == '1':
                    result = newOrderList(curUserId, productList, out_trade_show_no, out_trade_no, sign, addrId)
                    pay_info['out_trade_show_no'] = out_trade_show_no
                else:
                    pay_info['out_trade_show_no'] = ''
                    result = updateOrderListOutTradeNoByOutTradeShowNoList(out_trade_no, outTradeShowNoList)
                print(pay_info)
                if result['rtnCode'] != 0:    ##操作失败
                    return HttpResponse(json.dumps(result), content_type="application/json")
                return HttpResponse(json.dumps(pay_info), content_type="application/json")
            return HttpResponse(json.dumps(err_json), content_type="application/json")
    
def getTotalFeeByOrderList(orderListObj):
    order_total_fee = 0
    for curOrder in orderListObj:
        order_price = curOrder.product_price
        order_total_fee += int(order_price * 100)
    return order_total_fee
def wxpay(request):
    '''
    支付回调通知
    :return:
    '''
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    if request.method == 'POST':
        try:
            data = xml_to_dict(request.data)
            print(data)
            result_code = data['result_code']
            sign = data['sign']
            total_fee = data['total_fee']
            openid = data['openid']
            out_trade_no = data['out_trade_no']
            orderListObj = OrderList.objects.filter(out_trade_no=out_trade_no)
        except Exception as e:
            logging.error(e)
        else:
            #print(data)
            if result_code == 'SUCESS':
                order_total_fee = getTotalFeeByOrderList(orderListObj)
                if order_total_fee == total_fee:
                    print('pay success')
                    for curOrder in orderListObj:
                        curOrder.order_status = DEFAULT_ORDER_SAVED_STATUS
                        curOrder.save()
                else:
                    print('pay fail')
        result_data = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }
        return HttpResponse(dict_to_xml(result_data), content_type="application/xml")
        #return dict_to_xml(result_data), {'Content-Type': 'application/xml'}