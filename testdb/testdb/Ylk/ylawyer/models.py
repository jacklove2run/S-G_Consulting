# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
# Create your models here.

class ProductInfo(models.Model):                  #产品信息表
    product_id = models.IntegerField("商品ID")
    product_name = models.CharField('商品名称', max_length=200, default='')
    product_price = models.FloatField('商品价格')
    product_desc = models.CharField('商品信息', max_length=1000, default='')
    product_img_url = models.CharField('图片地址', max_length=255, default='')
    
    product_address = models.CharField('服务地址', max_length=200, default='')
    service_type = models.CharField('服务方式：在线', max_length=200, default='')
    service_address = models.CharField('服务范围：北京', max_length=200, default='')
    service_way = models.CharField('服务期限', max_length=200, default='')
    service_time = models.CharField('办理时间', max_length=200, default='')      
    
    def __str__(self):
        return self.product_name    

        
        
class OrderList(models.Model):                   #订单信息表
    user_id = models.CharField('用户id', max_length=155)
    product_name = models.CharField('商品名称', max_length=200)
    product_desc = models.CharField('商品描述', max_length=200)
    product_price = models.FloatField('商品价格')
    #product_price = models.DecimalField('商品价格', max_digits=10, decimal_places=2)
    order_status = models.IntegerField('订单状态', default=1)
    img_url = models.CharField('图片地址', max_length=155)
    time = models.DateTimeField('下单时间', auto_now_add=True)
    out_trade_show_no = models.CharField('微信订单号', max_length=155, default='0') ##显示用
    out_trade_no = models.CharField('微信订单支付号', max_length=155, default='0')  ##支付用
    sign = models.CharField('微信支付回调验证签名', max_length=155)
    addr_id = models.CharField('订单地址id', max_length=155)
    def __str__(self):
        return self.product_name
    
class UserInfo(models.Model):
    user_id = models.CharField('用户微信id', max_length=155)
    user_wechat_name = models.CharField('用户微信昵称', max_length=155)
    user_img_url = models.CharField('用户微信头像', max_length=255, default='')
    name = models.CharField('用户姓名', max_length=255, default='')
    phone = models.CharField('用户手机号', max_length=15, default='')
    email = models.CharField('用户邮箱', max_length=255, default='')
    address = models.CharField('用户通信地址', max_length=255, default='')
    def __str__(self):
        return self.product_name
    
class SavedProductList(models.Model):        #用户收藏表
    user_id = models.CharField('用户微信id', max_length=155)
    saved_product_id = models.IntegerField("商品ID")   ##使用ProductInfo的key做外键方便多表查询
    
    def __str__(self):
        return self.product_name
    
class SessionOpenId(models.Model):
    trd_session = models.CharField('3rd_session', max_length=256)
    session_key = models.CharField('session_key', max_length=256)
    openId = models.CharField('用户唯一标识', max_length=256)
    user_id = models.AutoField(primary_key=True)
    time = models.DateTimeField('注册时间')
    #time = models.DateTimeField('下单时间', auto_now_add=True)
    
    def __str__(self):
    
        return self.product_name
        
class userAddrList(models.Model):
    user_id = models.CharField('3rd_session', max_length=256)
    addr_id = models.AutoField(primary_key=True)
    recipient_name = models.CharField('收件人', max_length=255, default='')
    recipient_phone = models.CharField('收件人手机号', max_length=15, default='')
    recipient_addr = models.CharField('收件人地址', max_length=255, default='')
    
