import logging
from django.db import transaction
from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from accounts.models import UserDetails, User
from accounts.serializers import (
    UserDetailSerializer, 
    LoginSerializer, 
    CustomPasswordResetSerializer, 
    SetNewPasswordSerializer,
    LogoutSerializer
)
from accounts.utils import get_domain
from accounts.tasks.send_email_celery import send_email_id_verification_email
from accounts.tasks.welcome_task import send_welcome_email
import jwt
from accounts.tasks.password_reset_email_task import send_password_reset_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import permissions
import os
from django.http import HttpResponsePermanentRedirect

logger = logging.getLogger("project_management")


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.getenv('APP_SCHEME'), 'http', 'https']
class RegistrationAPIView(generics.GenericAPIView):
    """Creates a new user in the system"""  

    serializer_class = UserDetailSerializer
    queryset = UserDetails.objects.all()

    def get_serializer_context(self):
        context = super(RegistrationAPIView, self).get_serializer_context()
        context.update({"http_method": self.request.method})
        return context
 
    def get(self, request, pk=None):
        try:
            if pk is None:
                users = UserDetails.objects.all()
                # serializer = UserDetailSerializer(users, context={"http_method": request.method}, many=True)
                serializer = self.get_serializer(users, many=True)
                return Response(serializer.data)
            
            try:
                user = UserDetails.objects.get(id=pk)
                # serializer = UserDetailSerializer(user, context={"http_method": request.method})
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except:
                return Response(f"User does not exists at id:{pk}")

        except Exception as e:
            logger.error(dict(message="error while showing the user",
                              class_name="RegistrationAPIView",
                              request_method="GET",
                              method_name="get",
                              errors=e))
            raise APIException(e)

    @transaction.atomic
    def post(self, request):
        try:
            # serializer = UserDetailSerializer(data=request.data, context={"http_method": request.method})
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                user_id = serializer.data['user']['id']
                current_site = get_domain(request)
                send_email_id_verification_email.delay(current_site, user_id)

                return Response({
                    "user": serializer.data, 
                    "status": status.HTTP_201_CREATED,
                    "message": "Verify Email To Login"
                    })

            return Response({"errors": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})
        except Exception as e:
            logger.error(dict(message="error while creating the user",
                              class_name="RegistrationAPIView",
                              request_method="POST",
                              method_name="post",
                              errors=e))
            raise APIException(e)


    def patch(self, request, pk):
        try:
            user = UserDetails.objects.get(id=pk)
        except:
            return Response(f"User does not exists at id:{pk}")
        # serializer = UserDetailSerializer(user, data=request.data, partial=True, context={"http_method": request.method})
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "success": "User updated successfully"
            })

        return Response({"errors": serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

class VerifyEmail(generics.GenericAPIView):

    def get(self, request):
        token = request.GET.get("token")
        try:
            # decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, options={"verify_signature": False})
            user = User.objects.get(id=payload["user_id"]) 
            if not user.verification:
                user.verification = True
                user.save()
                user_first_name = user.first_name
                to_email = user.email
                current_site = get_domain(request)
                send_welcome_email.run(current_site, user_first_name, to_email)
            return Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"email": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"email": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordResetAPIView(generics.GenericAPIView):

    serializer_class = CustomPasswordResetSerializer

    def post(self, request):
        email = request.data["email"]
        if User.objects.filter(email=email).exists():
            user_id = User.objects.get(email=email).id
            current_site = get_domain(request)
        
            redirect_url = request.data.get("redirect_url", "")
            send_password_reset_email.delay(redirect_url, current_site, user_id)

        return Response({"success": "We have sent you a link to reset your password"}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPIView(generics.GenericAPIView):

    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+"?token_valid=False")
                    # return Response({"error": "Token is not valid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return CustomRedirect(os.getenv('FE_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
                # return Response({"success": True, "message": "Credentials valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
            else:
                return CustomRedirect(os.getenv('FE_URL', '')+'?token_valid=False')
            

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return CustomRedirect(redirect_url+"?token_valid=False")
                # return Response({"error": "Token is not valid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):

    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True, "message": "Password Reset Sucesss"}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):

    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)