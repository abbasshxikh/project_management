from functools import partial
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
from rest_framework.renderers import TemplateHTMLRenderer
from django.db import transaction

# from rest_auth.views import LoginView as RestLoginView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_auth.serializers import LoginSerializer
from django.contrib.auth import login
from rest_auth.views import LoginView as RestLoginView

logger = logging.getLogger("project_system")


class RegistrationAPIView(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'register.html'
    # serializer_class = UserDetailSerializer

    def get(self, request, pk=None):
        try:
            if pk is None:
                users = UserDetails.objects.all()
                serializer = UserDetailSerializer(
                    users, context={"method": request.method}, many=True
                )
                return Response(serializer.data)

            user = UserDetails.objects.get(id=pk)
            serializer = UserDetailSerializer(user, context={"method": request.method})
            return Response(serializer.data)
        except Exception as e:
            logger.error(
                dict(
                    message="error while showing the user details",
                    class_name="RegistrationAPIView",
                    request_method="GET",
                    method_name="get",
                    errors=e,
                )
            )
            raise APIException(e)

    @transaction.atomic()
    def post(self, request):
        try:
            serializer = UserDetailSerializer(
                data=request.data, context={"method": request.method}
            )
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

    def patch(self, request, pk, format=None):
        try:
            users = UserDetails.objects.get(id=pk)
            serializer = UserDetailSerializer(
                users,
                context={"method": request.method},
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "Message": "Your Data is updated...",
                        "User": serializer.data,
                        "Status": status.HTTP_201_CREATED,
                    }
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(
                dict(
                    message="error while updating user",
                    class_name="RegistrationAPIView",
                    request_method="PATCH",
                    method_name="patch",
                    errors=e,
                )
            )
            raise APIException(e)

    def delete(self, request, pk, format=None):
        try:
            users = UserDetails.objects.get(id=pk)
            users.delete()
            return Response({"Message": "User deleted successfully..."})
        except Exception as e:
            logger.error(
                dict(
                    message="error while deleting  user",
                    class_name="RegistrationAPIView",
                    request_method="DELETE",
                    method_name="delete",
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


class DepartmentApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "dept_list.html"

    def get(self, request):
        queryset = Department.objects.all()
        return Response({"profiles": queryset})
