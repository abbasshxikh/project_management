from django.contrib.contenttypes import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Department, Designation, TechnologyStack, UserDetails

# from rest_auth.serializers import LoginSerializer


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

    email = serializers.EmailField(max_length=50, min_length=6)
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

    def validate(self, args):
        email = args.get("email", None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ("email already exists")})
        return super().validate(args)


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
