"""Ylk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ylawyer import dbcontroller
from ylawyer import login
urlpatterns = [
    url(r"^order/get_order_list/(?P<trd_session>\S+)$", dbcontroller.getOrderList),
    url(r"^order/get_unsaved_order_list/(?P<trd_session>\S+)$", dbcontroller.getUnsavedOrderList),
    url(r"^user/get_user_info/(?P<trd_session>\S+)$", dbcontroller.getUserInfo),
    url(r"^commodity/get_commodity_detail/(?P<cur_product_id>\d+)$", dbcontroller.getProductInfo),
    url(r"^user/set_user_info", dbcontroller.updateUserInfo),
    url(r"^order/get_saved_list/(?P<trd_session>\S+)$", dbcontroller.getSavedProductList),
    url(r"^commodity/buy_commodity$", dbcontroller.setProductState),
    url(r"^product/get_all_productinfo$", dbcontroller.getAllProductList),
    url(r"^commodity/get_commodity_status/(?P<cur_product_id>\S+)/(?P<trd_session>\S+)$", dbcontroller.getProductStoredInfo),
    url(r"^auth/oauth$", login.get_login_session),
    url(r"^address/set_recv_address$", dbcontroller.setRecOrderAddr),
    url(r"^address/add_recv_address$", dbcontroller.addRecvOrderAddr),
    url(r"^address/add_get_address/(?P<trd_session>\S+)$", dbcontroller.getRecvOrderAddr), 
    url(r"^address/del_recv_address$", dbcontroller.deleteRecvOrderAddr)
    url(r"^order/wxpay/create_pay$", app.create_pay),
    url(r"^order/wxpay/notify$", app.wxpay)
]
