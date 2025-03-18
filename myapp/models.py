from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

class offer(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    isactive = models.BooleanField(default=True)

class arrivals(models.Model):
    type = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)

class StoreItem(models.Model):
    Gender_Choice = [
        ('M','Male'),
        ('F','Female'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    gender = models.CharField(max_length=1,choices=Gender_Choice)
    image = models.ImageField(upload_to='images', blank=True, null=True)

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('myapp.StoreItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def total_price(self):
        return self.quantity * self.product.price
