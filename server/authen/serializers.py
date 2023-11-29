from rest_framework import serializers
from .models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password can't be empty!")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User doesn't exist!")

        return data


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User email need to be unique!")

        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
