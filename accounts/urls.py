from django.urls import path
from accounts.views import (
    RegistrationAPIView,
    LoginView,
    DepartmentApiView,
    EmailValidate,
)


urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("register/<int:pk>/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("activate/<uidb64>/<token>/", EmailValidate.as_view(), name="activate"),
    path("dept/", DepartmentApiView.as_view(), name="deptarment"),
]
