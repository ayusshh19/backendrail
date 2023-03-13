from rest_framework import serializers
from .models import Userregister,Usercoupon,Delivery,Productpurchase,Order


class Registerserializer(serializers.ModelSerializer):
    class Meta:
        model=Userregister
        fields='__all__'
        
class Usercouponserializer(serializers.ModelSerializer):
    class Meta:
        model=Usercoupon
        fields='__all__'

class Deliveryserializer(serializers.ModelSerializer):
    class Meta:
        model=Delivery
        fields='__all__'

class Productpurchaseserializer(serializers.ModelSerializer):
    class Meta:
        model=Productpurchase
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2