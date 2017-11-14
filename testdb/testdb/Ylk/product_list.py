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
import logging

     

PRODUCT_LIST = [
        {
            'tabId' : '1', 
            'name' : '常用推荐', 
            'tab_img_url' : 'https://weizhilawyers.com/static/22.jpg',
            'services' : 
            [
                {
                    'product_id' : '1', 
                    'product_name' : '写合同', 
                    'product_price' : '500', 
                    'product_desc' : '职业律师代写', 
                    'product_img_url' : 'https://weizhilawyers.com/static/1.jpg'
                }, 
                {
                    'product_id' : '2', 
                    'product_name' : '审合同', 
                    'product_price' : '300', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/2.jpg'
                }
            ]
        },
        {
            'tabId' : '2', 
            'name' : '合同服务', 
            'tab_img_url' : 'https://weizhilawyers.com/static/22.jpg',
            'services' : 
            [
                {
                    'product_id' : '1', 
                    'product_name' : '写合同', 
                    'product_price' : '500', 
                    'product_desc' : '职业律师代写', 
                    'product_img_url' : 'https://weizhilawyers.com/static/1.jpg'
                }, 
                {
                    'product_id' : '2', 
                    'product_name' : '审合同', 
                    'product_price' : '300', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/2.jpg'
                },
                {
                    'product_id' : '3', 
                    'product_name' : '写诉状', 
                    'product_price' : '2000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/3.jpg'
                },
                {
                    'product_id' : '4', 
                    'product_name' : '写答辩状', 
                    'product_price' : '5000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/4.jpg'
                },
                {
                    'product_id' : '5', 
                    'product_name' : '写劳动仲裁申请书', 
                    'product_price' : '5000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/5.jpg'
                }
            ]
        },
        {
            'tabId' : '3', 
            'name' : '谈判服务', 
            'tab_img_url' : 'https://weizhilawyers.com/static/22.jpg',
            'services' : 
            [
                {
                    'product_id' : '6', 
                    'product_name' : '个人谈判', 
                    'product_price' : '1000', 
                    'product_desc' : '职业律师谈判服务', 
                    'product_img_url' : 'https://weizhilawyers.com/static/6.jpg'
                }, 
                {
                    'product_id' : '7', 
                    'product_name' : '公司谈判', 
                    'product_price' : '2000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/7.jpg'
                }
            ]
        },
        {
            'tabId' : '4', 
            'name' : '诉讼服务', 
            'tab_img_url' : 'https://weizhilawyers.com/static/22.jpg',
            'services' : 
            [
                {
                    'product_id' : '8', 
                    'product_name' : '指导打官司', 
                    'product_price' : '2000', 
                    'product_desc' : '职业律师诉讼服务', 
                    'product_img_url' : 'https://weizhilawyers.com/static/8.jpg'
                }, 
                {
                    'product_id' : '9', 
                    'product_name' : '代理打官司', 
                    'product_price' : '5000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/9.jpg'
                }
            ]
        },
        {
            'tabId' : '5', 
            'name' : '个人代办', 
            'tab_img_url' : 'https://weizhilawyers.com/static/22.jpg',
            'services' : 
            [
                {
                    'product_id' : '10', 
                    'product_name' : '代办遗嘱', 
                    'product_price' : '2000', 
                    'product_desc' : '职业律师诉讼服务', 
                    'product_img_url' : 'https://weizhilawyers.com/static/10.jpg'
                }, 
                {
                    'product_id' : '11', 
                    'product_name' : '代办公证', 
                    'product_price' : '2000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/11.jpg'
                },
                {
                    'product_id' : '12', 
                    'product_name' : '代办社保', 
                    'product_price' : '1000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/12.jpg'
                }
            ]
        },
        {
            'tabId' : '6', 
            'name' : '公司代办', 
            'tab_img_url' : 'https://weizhilawyers.com/static/22.jpg',
            'services' : 
            [
                {
                    'product_id' : '13', 
                    'product_name' : '公司注册', 
                    'product_price' : '2000', 
                    'product_desc' : '职业律师诉讼服务', 
                    'product_img_url' : 'https://weizhilawyers.com/static/13.jpg'
                }, 
                {
                    'product_id' : '14', 
                    'product_name' : '商标注册', 
                    'product_price' : '2000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/14.jpg'
                },
                {
                    'product_id' : '15', 
                    'product_name' : '内部制度建设', 
                    'product_price' : '1000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/15.jpg'
                },
                {
                    'product_id' : '16', 
                    'product_name' : '专项法律培训', 
                    'product_price' : '1000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/16.jpg'
                }
            ]
        },
        {
            'tabId' : '7', 
            'name' : '公司法务外包', 
            'tab_img_url' : 'https://weizhilawyers.com/static/22.jpg',
            'services' : 
            [
                {
                    'product_id' : '17', 
                    'product_name' : '创业公司专属法务（试用版）', 
                    'product_price' : '1000', 
                    'product_desc' : '职业律师诉讼服务', 
                    'product_img_url' : 'https://weizhilawyers.com/static/17.jpg'
                }, 
                {
                    'product_id' : '18', 
                    'product_name' : '创业公司专属法务（季度版）', 
                    'product_price' : '3000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/18.jpg'
                },
                {
                    'product_id' : '19', 
                    'product_name' : '创业公司专属法务（年度版）', 
                    'product_price' : '6000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/19.jpg'
                },
                {
                    'product_id' : '20', 
                    'product_name' : '公司专属法务（基础版）', 
                    'product_price' : '10000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/20.jpg'
                },
                {
                    'product_id' : '21', 
                    'product_name' : '公司专属法务（升级版）', 
                    'product_price' : '20000', 
                    'product_desc' : '细致入微，不会放过一个细节', 
                    'product_img_url' : 'https://weizhilawyers.com/static/21.jpg'
                }
            ]
        }
    ]

    
PRODUCT_PIC_LIST = [
    'https://weizhilawyers.com/static/1.jpg',
    'https://weizhilawyers.com/static/2.jpg',
    'https://weizhilawyers.com/static/3.jpg',
    'https://weizhilawyers.com/static/4.jpg',
    'https://weizhilawyers.com/static/5.jpg',
    'https://weizhilawyers.com/static/6.jpg',
    'https://weizhilawyers.com/static/7.jpg',
    'https://weizhilawyers.com/static/8.jpg',
    'https://weizhilawyers.com/static/9.jpg',
    'https://weizhilawyers.com/static/10.jpg',
    'https://weizhilawyers.com/static/11.jpg',
    'https://weizhilawyers.com/static/12.jpg',
    'https://weizhilawyers.com/static/13.jpg',
    'https://weizhilawyers.com/static/14.jpg',
    'https://weizhilawyers.com/static/15.jpg',
    'https://weizhilawyers.com/static/16.jpg',
    'https://weizhilawyers.com/static/17.jpg',
    'https://weizhilawyers.com/static/18.jpg',
    'https://weizhilawyers.com/static/19.jpg',
    'https://weizhilawyers.com/static/20.jpg',
    'https://weizhilawyers.com/static/21.jpg'
]
    
def setProductInfoList(reqeust):
    productList = PRODUCT_LIST
    for productInfo in productList:
        for product in productInfo['services']:
            product_id = product['product_id']
            product_name = product['product_name']
            product_price = product['product_price']
            product_desc = product['product_desc']
            product_img_url = product['product_img_url']
            product_address = '北京'
            service_type = '在线'
            service_address = '北京'
            service_time = '一周'
            try:
                productInfoObj = ProductInfo.objects.get(product_id=product_id)
                productInfoObj.product_price = product_price
                productInfoObj.save()
            except:
                productInfoObj = ProductInfo(product_id=product_id, product_name=product_name, product_price=product_price, product_desc=product_desc, product_img_url=product_img_url, product_address=product_address, service_type=service_type, service_address=service_address, service_time=service_time)
                productInfoObj.save()
    success_json = {'rtnCode' : 0, 'rtnMsg' : 'update product info list success'}
    return HttpResponse(json.dumps(success_json), content_type="application/json")   