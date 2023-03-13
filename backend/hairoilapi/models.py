from django.db import models
import uuid
# Create your models here.

def generate_uuid():
    return str(uuid.uuid4())

class Userregister(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    registertime=models.TimeField(auto_now_add=True)
    issseller=models.BooleanField(default=False)
    isadmin=models.BooleanField(default=False)
    unique_id = models.UUIDField(default=generate_uuid, editable=False, unique=True)
    
class Usercoupon(models.Model):
    userid=models.ForeignKey(Userregister,on_delete=models.CASCADE)
    no_of_coupon=models.IntegerField(default=0)
    
class Productpurchase(models.Model):
    userid=models.ForeignKey(Userregister,on_delete=models.CASCADE)
    productprice=models.CharField(max_length=100)
    productname=models.CharField(max_length=100)
    purchasetime=models.TimeField(auto_now_add=True)
    paymentcompletion=models.BooleanField(default=False)
    sellerstatus=models.BooleanField(default=False)
    
class Delivery(models.Model):
    prodid=models.ForeignKey(Productpurchase,on_delete=models.CASCADE)
    buildingaddress=models.CharField(max_length=100,default='')
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    address=models.CharField(max_length=1000)
    landmark=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    
class Order(models.Model):
    userid=models.ForeignKey(Userregister,default='',on_delete=models.CASCADE)
    prodid=models.ForeignKey(Productpurchase,default='',on_delete=models.CASCADE)
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_product