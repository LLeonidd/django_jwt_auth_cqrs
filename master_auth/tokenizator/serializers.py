from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .tokens import CustomToken


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Кастомный серилизатор для вывода данных при обновлении токена
    """
    token_class = CustomToken

    def validate(self, attrs):
        data = super().validate(attrs)
        data = {
            'tokens': data,
        }
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный серилизатор для вывода данных при запросе пары токенов (доступа, обновлении)
    """
    token_class = CustomToken

    def validate(self, attrs):
        data = super().validate(attrs)
        data = {
            'tokens': data,
        }
        return data

