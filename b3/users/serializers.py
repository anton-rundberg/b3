from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utils.fields import LowerCaseEmailField

from . import models


class AccessTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


class RegistrationSerializer(serializers.ModelSerializer):
    email = LowerCaseEmailField(
        validators=[
            UniqueValidator(queryset=models.User.objects.all(), lookup="iexact")
        ]
    )
    password = serializers.CharField(
        validators=[validate_password],
        style={"input_type": "password"},
        write_only=True,
    )

    class Meta:
        model = models.User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.SlugRelatedField(
        slug_field="email__iexact",
        queryset=models.User.objects.all(),
        write_only=True,
    )


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):
    INVALID_TOKEN_ERROR = "Invalid token"

    password = serializers.CharField(
        validators=[validate_password],
        style={"input_type": "password"},
        write_only=True,
    )
    token = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ("password", "token")

    def validate_token(self, token):
        user = self.instance
        token_is_valid = default_token_generator.check_token(user, token)
        if not token_is_valid:
            raise serializers.ValidationError(self.INVALID_TOKEN_ERROR)

        return token

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    CURRENT_PASSWORD_INCORRECT_ERROR = "Current password was incorrect"

    current_password = serializers.CharField(
        label="Current password",
        source="password",
        write_only=True,
    )
    new_password = serializers.CharField(
        label="New password",
        validators=[validate_password],
        write_only=True,
    )

    class Meta:
        model = models.User
        fields = ("current_password", "new_password")

    def validate_current_password(self, current_password):
        if not self.context["request"].user.check_password(current_password):
            raise serializers.ValidationError(self.CURRENT_PASSWORD_INCORRECT_ERROR)
        return current_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance


class UserMeSerializer(serializers.ModelSerializer):
    email = LowerCaseEmailField(
        validators=[
            UniqueValidator(queryset=models.User.objects.all(), lookup="iexact")
        ]
    )

    class Meta:
        model = models.User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_staff",
        )


class LoginSerializer(serializers.Serializer):
    INCORRECT_EMAIL_OR_PASSWORD_MSG = "Incorrect email or password."
    email = LowerCaseEmailField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        required=True,
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")

        user = authenticate(request, email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                self.INCORRECT_EMAIL_OR_PASSWORD_MSG, code="authorization"
            )

        attrs["user"] = user
        return attrs
