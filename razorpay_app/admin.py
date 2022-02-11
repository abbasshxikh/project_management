from django.contrib import admin
from razorpay_app.models import Payment

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("name", "paid")