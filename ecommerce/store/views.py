from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .forms import customform
from django.urls import reverse_lazy,reverse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def store(req):
    if req.user.is_authenticated:
        customer=req.user.customer 
        orders,created=order.objects.get_or_create(customer=customer,complete=False)
        items=orders.orderitem_set.all()
        cartitems=orders.cart_items
    else:
        items=[]
        orders={"cart_total":0,"cart_items":0,"shipping":False}
        cartitems=orders["cart_items"]

    products=product.objects.all()
    context={"products":products,"cartitems":cartitems}
    return render(req,"store/store.html",context)
@login_required
def cart(req):
    if req.user.is_authenticated:
        customer=req.user.customer 
        orders,created=order.objects.get_or_create(customer=customer,complete=False)
        items=orders.orderitem_set.all()
        cartitems=orders.cart_items
    else:
        items=[]   
        orders={"cart_total":0,"cart_items":0,"shipping":False}
        cartitems=orders["cart_items"]
    context={"items":items,"orders":orders,"cartitems":cartitems}
    return render(req,"store/cart.html",context)

@login_required
def checkout(req):
    if req.user.is_authenticated:
        customer=req.user.customer 
        orders,created=order.objects.get_or_create(customer=customer,complete=False)
        items=orders.orderitem_set.all()
        cartitems=orders.cart_items 
    else:
        items=[]
        orders={"cart_total":0,"cart_items":0,"shipping":False}
        cartitems=orders["cart_items"]    
    context={"items":items,"orders":orders,"cartitems":cartitems}    
    return render(req,"store/checkout.html",context)

#@csrf_exempt
def updateitem(request):
    data=json.loads(request.body)
    productid=data["productid"]
    action=data["action"]

    print("action: ",action)
    print("productid: ",productid)

    customer=request.user.customer
    products=product.objects.get(id=productid)
    orders,created=order.objects.get_or_create(customer=customer,complete=False)
    orderitems,created=orderitem.objects.get_or_create(order=orders,product=products)
    if action=="add":
        orderitems.quantity=(orderitems.quantity+1)
    elif action=="remove":
        orderitems.quantity=(orderitems.quantity-1)
    orderitems.save()

    if orderitems.quantity<=0:
        orderitems.delete()
    return JsonResponse("item was added",safe=False)
    
def processorder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    
    if request.user.is_authenticated:
        customer=request.user.customer
        orders,created=order.objects.get_or_create(customer=customer,complete=False)
        orders.transaction_id=transaction_id
        total=float(data["form"]["total"])
        if total==float(orders.cart_total):
            orders.complete=True
        orders.save()
        if orders.shipping==True:
            shippingaddress.objects.create(customer=customer,order=orders,address=data["shipping"]["address"],city=data["shipping"]["city"],state=data["shipping"]["state"],zipcode=data["shipping"]["zipcode"])  
    else:
        print("user is not authenticaed")        
    return JsonResponse("payment completed",safe=False)   

def register(req):
    form=UserCreationForm()
    if req.POST:
        form=UserCreationForm(req.POST)
        user=form.save()
        name=req.POST["name"]
        email=req.POST["email"]
        obj=customer.objects.create(user=user,name=name,email=email)
        obj.save()
        return redirect(reverse("login"))
    else:
        return render(req,"registration/signup.html",{"form":form})
    
