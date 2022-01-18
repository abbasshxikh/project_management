from django.urls import path
from accounts.views import RegistrationAPIView, LoginView, DepartmentApiView


urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("register/<int:pk>/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("dept/", DepartmentApiView.as_view(), name="deptarment"),
]
