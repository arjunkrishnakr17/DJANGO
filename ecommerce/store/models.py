from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=200,null=True)

    def __str__(self):
        return self.name

class product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name
    @property
    def imageurl(self):
        try:
            url=self.image.url
        except:
            url=""
        return url        

class order(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_orderd=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping        

    
    @property
    def cart_total(self):
        total=0
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            total+=i.total 
        return total
    @property
    def cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([i.quantity for i in orderitems])
        return total

class orderitem(models.Model):
    product=models.ForeignKey(product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,blank=True,null= True)
    date_added=models.DateField(auto_now_add=True) 

    @property
    def total(self):
        total=self.product.price*self.quantity
        return total

class shippingaddress(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    
    


