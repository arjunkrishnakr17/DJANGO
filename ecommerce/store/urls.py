from django.urls import path
from . import views

urlpatterns=[
    path("",views.store,name="store"),
    path("cart/",views.cart,name="cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("update_item/",views.updateitem,name="updateitem"),
    path("process_order/",views.processorder,name="processorder"),
    path("signup/",views.register,name="signup"), 
]