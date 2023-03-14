from django.urls import path,include
from .views import home,registerUser,Purchase,Customeraddress,coupon,adminpanel,loginuser,start_payment,handle_payment_success,purchasecompletion
urlpatterns = [
    path('', home,name='home'),
    path('register/', registerUser,name='register'),
    path('login/', loginuser,name='login user'),
    path('purchase/', Purchase,name='Purchased products'),
    path('address/', Customeraddress,name='Customer address'),
    path('coupon/', coupon,name='User Coupon'),
    path('adminpanel/', adminpanel,name='admin panel'),
    path('pay/', start_payment, name="payment"),
    path('completepay/', purchasecompletion, name="payment"),
    path('payment/success/', handle_payment_success, name="payment_success")
    
]
