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

urlpatterns = [
	url(r"^/order/get_order_list/(?P<user_id>\d+)$", dbcontroller.getOrderList),
	url(r"^/user/get_user_info/(?P<user_id>\d+)$", dbcontroller.getUserInfo),
	url(r"^/commodity/get_commodity_detail/(?P<cur_product_id>\d+)$", dbcontroller.getProductInfo),
	url(r"^/user/set_user_info/", dbcontroller.updateUserInfo),
	url(r"^/order/get_saved_list/(?P<cur_user_id>\d+)$", dbcontroller.getSavedProductList),
	url(r"^/commodity/buy_commodity/$", dbcontroller.setProductState)
]
