import email
from statistics import mode
from tkinter import N
from django.db import models


# Create your models here.

class Payment(models.Model):

    name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=100)
    order_id = models.CharField(max_length=1000, blank=True)
    razorpay_payment_id = models.CharField(max_length=1000 ,blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)