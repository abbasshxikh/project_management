from typing_extensions import Required
from django.contrib.contenttypes import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Department, Designation, TechnologyStack, UserDetails
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.serializers import LoginSerializer, PasswordResetSerializer
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormCore
from django import forms
from accounts.tasks.passwors_reset_task import send_password_reset_email


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "name",
        )


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = (
            "id",
            "name",
        )


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    #  email = serializers.EmailField(
    #     validators=[
    #         UniqueValidator(
    #             queryset=User.objects.all(),
    #             message="This email is already register by user.",
    #         )
    #     ]
    # )
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "past_experience",
            "email",
            "password",
        )

    def validate_email(self, email):
        # if self.context.get("is_create"):
        if self.context["method"] == "POST":
            if email:
                if User.objects.filter(email=email).exists():
                    raise serializers.ValidationError(
                        "A user is already registered with this e-mail address."
                    )
        return email


class CustomLoginSerializer(LoginSerializer):

    # def get_queryset(self):
    #     if self.request.user.verification:
    #         print('is there a verified email address?')
    #         print(User.objects.filter(user=self.request.user, verification=False))

    # def validate(self, data):
    #     user = authenticate(**data)
    #     if user:
    #         if user.verification:
    #             data['user'] = user  # added user model to OrderedDict that serializer is validating
    #             return data  # and in sunny day scenario, return this dict, as everything is fine
    #         raise exceptions.AuthenticationFailed('Account is not verified')
    #     raise exceptions.AuthenticationFailed()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get("user").verification:
            return attrs
        raise serializers.ValidationError(
            {"email": "Please verify your email to login"}
        )


class TechnologyStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnologyStack
        fields = (
            "id",
            "name",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    user = RegistrationSerializer()
    technology_stack = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TechnologyStack.objects.all()
    )

    class Meta:
        model = UserDetails
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        technology_stack = validated_data.pop("technology_stack")
        user_obj = User.objects.create(**user)
        user_obj.set_password(user["password"])
        user_obj.save()
        user_details = UserDetails.objects.create(user=user_obj, **validated_data)
        user_details.technology_stack.set(technology_stack)
        return user_details

    def __init__(self, *args, **kwargs):
        super(UserDetailSerializer, self).__init__(*args, **kwargs)

        if self.context["method"] == "GET":
            self.fields["technology_stack"] = TechnologyStackSerializer(many=True)
            self.fields["department"] = DepartmentSerializer()
            self.fields["designation"] = DesignationSerializer()

    def update(self, instance, validated_data):
        user = validated_data.get("user")
        validated_data.pop("email", None)
        # del user['email']
        instance.user.first_name = user.get("first_name")
        instance.user.last_name = user.get("last_name")
        instance.user.past_experience = user.get("past_experience")
        instance.user.save()
        technology_stack = validated_data.pop("technology_stack")
        instance.technology_stack.set(technology_stack)
        instance.department = validated_data.get("department", instance.department)
        instance.designation = validated_data.get("designation", instance.designation)
        instance.joining_date = validated_data.get(
            "joining_date", instance.joining_date
        )
        instance.completion_date = validated_data.get(
            "completion_date", instance.completion_date
        )
        instance.save()
        return instance


class PasswordResetForm(PasswordResetFormCore):
    """custom password reset form for send email with celery"""

    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "email", "placeholder": "Email"}
        ),
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        # print(subject_template_name)
        # print(email_template_name)
        context["user"] = context["user"].id
        # print("hh",context)
        send_password_reset_email.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name,
        )


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """Password Reset Serializer"""

    def get_email_options(self):
        return {"email_template_name": "commerce_api/password_reset_email.txt"}

    def validate_email(self, value):
        self.reset_form = PasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError("Error")

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Invalid e-mail address")
        return value
