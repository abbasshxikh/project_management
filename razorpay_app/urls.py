from django.urls import path
from razorpay_app.views import (
    HomeView,
    SuccessView
)

app_name = 'razorpay_app'


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("success/", SuccessView.as_view(), name="success")
]
