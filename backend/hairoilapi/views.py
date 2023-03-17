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
        prodid=request.data['prodid']
        product=Productpurchase.objects.filter(id=prodid).update(paymentcompletion=True)
        prodobj=Productpurchase.objects.filter(id=prodid)
        productserializer=Productpurchaseserializer(prodobj,many=True)
        return Response({'msg':productserializer.data},status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def returnpayment(request):
    if request.method=='GET':
        return Response({'msg':'Pay return payment'},status=status.HTTP_200_OK)
    
    if request.method=='POST':
        prodid=request.data['prodid']
        product=Productpurchase.objects.filter(id=prodid).update(sellerstatus=True)
        prodobj=Productpurchase.objects.filter(id=prodid)
        productserializer=Productpurchaseserializer(prodobj,many=True)
        return Response({'msg':productserializer.data},status=status.HTTP_200_OK)
    
@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
    amount = request.data['amount']
    name = request.data['name']

    # setup razorpay client this is the client to whome user is paying money that's you
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
    payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
    order = Order.objects.create(order_product=name, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = OrderSerializer(order)
    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)


@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])
    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""
    
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)
    purchaseorder=Productpurchase.objects.get(id=request.data['pid'])
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
    purchaseorder.paymentcompletion=True
    purchaseorder.save()
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)
@api_view(['GET'])
def returnpayadd(request):
    if request.method=='GET':
            try:
              cartproducts=Productpurchase.objects.latest()
              getaddress=Delivery.objects.latest()
              productserializer=Productpurchaseserializer(cartproducts,many=True)
              addresserializer=Deliveryserializer(getaddress,many=True)
              return Response({'productlist':productserializer.data,'addresslist':addresserializer.data},status=status.HTTP_200_OK)
            except:
              return Response({'msg':'something went wrong!!!'},status=status.HTTP_200_OK)
    return Response({'msg':'something went wrong!!!'},status=status.HTTP_200_OK)