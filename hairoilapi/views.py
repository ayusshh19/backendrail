from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import environ
import razorpay
from .serializers import Registerserializer,Productpurchaseserializer,Deliveryserializer,Usercouponserializer,OrderSerializer
from .models import Userregister,Usercoupon,Productpurchase,Delivery,Order
import json
# Create your views here.
env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


@api_view(['GET','POST'])
def home(request):
    return Response({'msg':'Welcome user to our ecommerce'},status=status.HTTP_200_OK)

@api_view(['GET','POST'])        
def loginuser(request):
    if request.method=='GET':
        return Response({'msg':'Welcome user login to proceed!!'},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        email=request.data['email']
        password=request.data['password']
        try:
          userexist=Userregister.objects.filter(email=email,password=password)
          print(userexist)
          if userexist:
              request.session['email']=email
              userserial=Registerserializer(userexist,many=True)
              return Response({'msg':'successfully logged in!!','user':userserial.data},status=status.HTTP_200_OK)
          return Response({'msg':'Pls register yourself before login!!'},status=status.HTTP_404_NOT_FOUND)
        except :
          return Response({'msg':'Something went wrong!!'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET','POST'])
def registerUser(request):
    if request.method=='GET':
        return Response({'msg':'Please register yourself'},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        serializers=Registerserializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            request.session['username']=request.data['username']
            return Response({'msg':'You have registered successfully!!'},status=status.HTTP_200_OK)
        return Response({'msg':serializers.errors},status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST'])
def Purchase(request):
    if request.method=='GET':
        return Response({'msg':'Please Select Products'},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        username=request.data['username']
        userobj=Userregister.objects.get(username=username)
        request.data['userid']=userobj.id
        serializers=Productpurchaseserializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'msg':'Payment Successfull Thank you!!','proddata':serializers.data},status=status.HTTP_200_OK)
        return Response({'msg':serializers.errors},status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST'])
def Customeraddress(request):
    if request.method=='GET':
        return Response({'msg':'Please Enter Your address'},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        serializers=Deliveryserializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({'msg':'Your address is saved!!'},status=status.HTTP_200_OK)
        return Response({'msg':serializers.errors},status=status.HTTP_403_FORBIDDEN)

@api_view(['GET','POST','PUT','PATCH'])
def coupon(request):
    if request.method=='GET':
        return Response({'msg':'Make others Purchase to get coupon'})
    
    if request.method=='POST':
        data=request.data
        uniqueid=data['unique_id']
        try:
           userobj= Userregister.objects.get(unique_id=uniqueid)
           data['userid']=userobj.id
           my_object = Usercoupon.objects.update_or_create(id=data['userid'],defaults=data)
           my_object.no_of_coupon += 1
           my_object.save()
                # return Response({'msg':'Hurray New Coupon!!'},status=status.HTTP_200_OK)
           return Response({'msg':'Hurray New Coupon!!'},status=status.HTTP_403_FORBIDDEN)
        except:
          return Response({'msg':'SOMETHING WENT WRONG'},status=status.HTTP_403_FORBIDDEN)
        #    serializers=Usercouponserializer(data=request.data)
        #    if serializers.is_valid():
        #         serializers.save()
@api_view(['GET','POST'])        
def adminpanel(request):
    if request.method=='GET':
            try:
              userobj=Userregister.objects.all()
              cartproducts=Productpurchase.objects.all()
              getaddress=Delivery.objects.all()
              userserializer=Registerserializer(userobj,many=True)
              productserializer=Productpurchaseserializer(cartproducts,many=True)
              addresserializer=Deliveryserializer(getaddress,many=True)
              return Response({'userlist':userserializer.data,'productlist':productserializer.data,'addresslist':addresserializer.data},status=status.HTTP_200_OK)
            except:
              return Response({'msg':'something went wrong!!!'},status=status.HTTP_200_OK)
    return Response({'msg':'something went wrong!!!'},status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def purchasecompletion(request):
    if request.method=='GET':
        return Response({'msg':'Complete product purchase '},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        username=request.data['username']
        userobj=Userregister.objects.filter(username=username)
        product=Productpurchase.objects.filter(userid=userobj).update(paymentcompletion=True)
        productserializer=Productpurchaseserializer(product,many=True)
        return Response({'msg':productserializer.data},status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def returnpayment(request):
    if request.method=='GET':
        return Response({'msg':'Pay return payment'},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        username=request.data['username']
        userobj=Userregister.objects.filter(username=username)
        product=Productpurchase.objects.filter(userid=userobj).update(sellerstatus=True)
        productserializer=Productpurchaseserializer(product,many=True)
        return Response({'msg':productserializer.data},status=status.HTTP_200_OK)
    
@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    name = request.data['name']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # create razorpay order
    # the amount will come in 'paise' that means if we pass 50 amount will become
    # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
    # mumtiply it by 100 so it will be 50 rupees.
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    # we are saving an order with isPaid=False because we've just initialized the order
    # we haven't received the money we will handle the payment succes in next 
    # function
    order = Order.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)