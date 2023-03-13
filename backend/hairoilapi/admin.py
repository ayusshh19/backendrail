from django.contrib import admin
from .models import Userregister,Usercoupon,Delivery,Productpurchase,Order

@admin.register(Userregister)
class UserregisterAdmin(admin.ModelAdmin):
    list_display=[f.name for f in Userregister._meta.fields]

@admin.register(Delivery)
class Deliveryadmin(admin.ModelAdmin):
    list_display=[f.name for f in Delivery._meta.fields]

@admin.register(Productpurchase)
class cartitemadmin(admin.ModelAdmin):
    list_display=[f.name for f in Productpurchase._meta.fields]
    

@admin.register(Usercoupon)
class Usercouponadmin(admin.ModelAdmin):
    list_display=[f.name for f in Usercoupon._meta.fields]

@admin.register(Order)
class Orderadmin(admin.ModelAdmin):
    list_display=[f.name for f in Order._meta.fields]