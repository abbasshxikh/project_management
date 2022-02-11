from django.urls import path
from accounts.views import (
    LogoutAPIView, 
    RegistrationAPIView, 
    VerifyEmail,
    LoginAPIView, 
    PasswordTokenCheckAPIView, 
    RequestPasswordResetAPIView, 
    SetNewPasswordAPIView,

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name="user_register"),
    path('register/<int:pk>/', RegistrationAPIView.as_view(), name="user"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name="user_login"),
    path('logout/', LogoutAPIView.as_view(), name="user_logout"),

    path('request-reset-email/', RequestPasswordResetAPIView.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name="password-reset-confirm"),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name="password-reset-complete"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]