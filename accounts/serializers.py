from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import User, UserDetails, Department, Designation, TechnologyStack
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name",)


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ("id", "name",)


class TechnologyStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnologyStack
        fields = ("id", "name")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3, required=True)
    password = serializers.CharField(style={'input_type':'password'}, max_length=68, min_length=6, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_no", "past_experience", "password",)
        extra_kwargs = {'username': {'required': False}} 

    def validate_email(self, email):
        # if self.context.get("is_create"):
        if self.context["http_method"]=="POST":
            if email:
                if User.objects.filter(email=email).exists():
                    raise serializers.ValidationError("A user is already registered with this e-mail address.")
        return email


class UserDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    technology_stack = serializers.PrimaryKeyRelatedField(many=True, queryset=TechnologyStack.objects.all())

    def __init__(self, *args, **kwargs):
        super(UserDetailSerializer, self).__init__(*args, **kwargs)

        if self.context['http_method']=="GET":
            self.fields['technology_stack'] = TechnologyStackSerializer(many=True)
            self.fields['department'] = DepartmentSerializer()
            self.fields['designation'] = DesignationSerializer()

    class Meta:
        model = UserDetails
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        technology_stack = validated_data.pop("technology_stack")

        user_obj = User.objects.create(**user)
        user_obj.set_password(user['password'])
        user_obj.save()

        user_details = UserDetails.objects.create(user=user_obj, **validated_data)
        user_details.technology_stack.set(technology_stack)
        return user_details

    def update(self, instance, validated_data):
        user = validated_data.pop("user")
        technology_stack = validated_data.pop("technology_stack")

        del user['email']
        User.objects.filter(id=instance.user.id).update(**user)

        user_details = UserDetails.objects.filter(id=instance.id)
        user_details[0].technology_stack.set(technology_stack)

        user_details.update(**validated_data)
        return user_details


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, style={'input_type':'password'}, write_only=True)
    # tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])

        return {
            "access": user.tokens()["access"],
            "refresh": user.tokens()["refresh"]
        }

    class Meta:
        model = User
        fields = ("email", "password", "tokens")

    def validate(self, attrs):

        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        if not user.verification:
            raise AuthenticationFailed("Email is not verified")

        return {
            "email": user.email,
            "tokens": user.tokens
        }

class CustomPasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ("email",)
    
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)        

    class Meta:
        fields = ("password", "token", "uidb64")

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
    
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        "bad_token": ("Token is expired or invalid")
    }

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")


