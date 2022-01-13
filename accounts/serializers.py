from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Department, Designation

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

    def create(self, validated_data):
        user = super(RegistrationSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
