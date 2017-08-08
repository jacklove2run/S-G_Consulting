# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ProductInfo(models.Model):                  #产品信息表
    product_id = models.IntegerField("商品ID", max_length=11)
    product_name = models.CharField('商品名称', max_length=200, default='')
	product_price = models.IntegerField('商品价格', max_length=11, default=0)
	product_info = models.CharField('商品信息', max_length=65535, default='')
    product_img_url = models.CharField('图片地址', max_length=255, default='')
	
	def __str__(self):
        return self.product_name

class OrderList(models.Model):                   #订单信息表
    user_id = models.CharField('用户微信id', max_length=155)
	product_name = models.CharField('商品名称', max_length=200)
    product_price = models.IntegerField('商品价格', max_length=11, default=0)
    time = models.DateTimeField('下单时间', auto_now_add=True)
	
    def __str__(self):
        return self.product_name
	
class UserInfo(models.Model)                     #用户信息表
    user_id = models.CharField('用户微信id', max_length=155)
	user_wechat_name = models.CharField('用户微信昵称', max_length=155)
	user_img_url = models.CharField('用户微信头像', max_length=255, default='')
	name = models.CharField('用户姓名', max_length=255, default='')
	phone = models.CharField('用户手机号', max_length=15, default='')
	email = models.CharField('用户邮箱', max_length=255, default='')
	address = models.CharField('用户通信地址', max_length=255, default='')
	def __str__(self):
        return self.product_name
	
class SavedProductList(models.Model)	    #用户收藏表
    user_id = models.CharField('用户微信id', max_length=155)
	saved_product_id = models.ForeignKey('ProductInfo')   ##使用ProductInfo的key做外键方便多表查询