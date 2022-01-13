import logging
from django.shortcuts import render
from accounts.models import User, UserDetails, Department, Designation
from rest_framework.views import APIView
from rest_framework import generics
from accounts.serializers import RegistrationSerializer, UserDetailSerializer
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

# from rest_auth.views import LoginView as RestLoginView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_auth.serializers import LoginSerializer
from django.contrib.auth import login
from rest_auth.views import LoginView as RestLoginView

logger = logging.getLogger("project_system")


class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = UserDetailSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            department, created = Department.objects.get_or_create(
                name=request.data.get("department")
            )
            request.data.update({"department": department.id})
            designation, created = Designation.objects.get_or_create(
                name=request.data.get("designation")
            )
            request.data.update({"designation": designation.id})
            if serializer.is_valid():
                user = serializer.save()
                uid = urlsafe_base64_encode(force_bytes(user.user))
                token = Token.objects.create(user=user.user).key
                return Response(
                    {
                        "Message": "Thank you for registrations in system...",
                        "User": serializer.data,
                        "Status": status.HTTP_201_CREATED,
                    }
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(
                dict(
                    message="error while creating new user",
                    class_name="RegistrationAPIView",
                    request_method="POST",
                    method_name="post",
                    errors=e,
                )
            )
            raise APIException(e)


class LoginView(RestLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            # user.verification = True
            login(request, user)
            return super().post(request, format=None)
        except Exception as e:
            logger.error(
                dict(
                    message="Error while User Login",
                    class_name="LoginView",
                    request_method="POST",
                    method_name="post",
                    errors=e,
                )
            )
            raise APIException(e)
