from rest_framework import serializers
from django.db import transaction
from accounts.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'patronymic',
            'password', 'password2', 'phone', 'role'

        )
        extra_kwargs = {
            'username': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords don't match"})
        attrs['email'] = attrs['email'].lower()
        attrs['username'] = attrs['email']
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=3, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'tokens')

    @staticmethod
    def get_tokens(data):
        return User.objects.get(email=data['email']).tokens()

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        user = auth.authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'patronymic', 'phone', 'role',
            'is_can_create_tasks', 'is_have_access_to_tasks', 'is_can_add_customers',
            'is_can_add_workers', 'is_have_access_to_workers'
        )


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'patronymic',
            'password', 'phone', 'role'
        )
        extra_kwargs = {
            'username': {'read_only': True},
        }

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['email'] = attrs['email'].lower()
        attrs['username'] = attrs['email']
        if (
                attrs['role'] == User.Roles.worker and not user.is_can_add_workers
        ) or (
                attrs['role'] == User.Roles.customer and not user.is_can_add_customers
        ):
            raise serializers.ValidationError("You don't have permission to do this")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
