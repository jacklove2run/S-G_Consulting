from django.contrib import admin
from ylawyer import models
from ylawyer.models import ProductInfo, OrderList, UserInfo, SessionOpenId, SavedProductList, userAddrList


# Register your models here.


class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'product_price', 'product_desc', 'product_img_url', 'product_address', 'service_type', 'service_address', 'service_way', 'service_time')
    # 定义搜索框以哪些字段可以搜索
    search_fields = ('product_name', 'product_id')
    
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')

class OrderListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_name', 'product_price', 'product_desc', 'time')
    search_fields = ('user_id', 'product_name')
    
    
class userAddrListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'addr_id', 'recipient_name', 'recipient_phone', 'recipient_addr')
    # 定义搜索框以哪些字段可以搜索
    search_fields = ('user_id', 'recipient_name', 'recipient_phone', 'recipient_addr')
# 引用的固定格式，注册的model和对应的Admin，Admin放在后边
# 同样还有noregister方法：比如admin.site.noregister(Group)，把group这个表在admin中去掉（默认user和group都是注册到admin中的）
#admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(OrderList, OrderListAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(userAddrList, userAddrListAdmin)