from django.urls import path
from accounts.views import RegistrationAPIView, LoginView


urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="register"),
]
