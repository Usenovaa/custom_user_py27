from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import send_activation_code


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        min_length=4,
        required=True)
    password_confirm = serializers.CharField(
        min_length=4, required=True
    )
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)


    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
              "Пользователь с таким email уже существует"   
            )
        return email
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                "Пароли не совпадают"
            )
        return attrs

    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user
    


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return attrs





