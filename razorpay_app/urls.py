from django.urls import path
from razorpay_app.views import (
    PaymentHomeView,
    PaymentSuccessView
)

app_name = 'razorpay_app'


urlpatterns = [
    path("", PaymentHomeView.as_view(), name="home"),
    path("success/", PaymentSuccessView.as_view(), name="success")
]
