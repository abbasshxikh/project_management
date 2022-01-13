from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Department, Designation, TechnologyStack, UserDetails

# from rest_auth.serializers import LoginSerializer


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=50, min_length=6)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "contact_number",
            "past_experience",
            "email",
            "password",
        )

    def validate(self, args):
        email = args.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ("email already exists")})
        return super().validate(args)

    # def create(self, validated_data):
    #     user = super(RegistrationSerializer, self).create(validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user


class UserDetailSerializer(serializers.ModelSerializer):
    user = RegistrationSerializer()

    class Meta:
        model = UserDetails
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        first_name = user.get("first_name")
        last_name = user.get("last_name")
        contact_number = user.get("contact_number")
        past_experience = user.get("past_experience")
        email = user.get("email")
        password = user.get("password")

        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            past_experience=past_experience,
            email=email,
            password=password,
        )
        user_obj.set_password(password)
        user_obj.save()
        user_details = UserDetails.objects.create(user=user_obj, **validated_data)
        return user_details


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
