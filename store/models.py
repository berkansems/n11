from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=25,null=True,blank=True)
    email=models.EmailField(max_length=25,null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    price= models.DecimalField( max_digits=5, decimal_places=2)
    digital=models.BooleanField(default=False,null=True,blank=True)
    off=models.BooleanField(default=False,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

    # @property behaves like an attribute not like a method
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=True)
    transaction_id=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderItems=self.orderitem_set.all()
        total=sum([item.itemsPrice for item in orderItems])
        return total
#
    @property
    def get_cart_items(self):
        orderItems=self.orderitem_set.all()
        total = sum(item.quantity for item in orderItems)
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def itemsPrice(self):
        total= self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

