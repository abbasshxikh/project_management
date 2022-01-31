from django.urls import path
from accounts.views import (
    RegistrationAPIView,
    LoginView,
    DepartmentApiView,
    EmailValidate,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
)


urlpatterns = [
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("register/<int:pk>/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("activate/<uidb64>/<token>/", EmailValidate.as_view(), name="activate"),
    path("dept/", DepartmentApiView.as_view(), name="deptarment"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView().as_view(),
        name="password_reset_confirm",
    ),
]
