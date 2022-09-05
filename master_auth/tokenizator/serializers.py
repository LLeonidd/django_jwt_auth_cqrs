from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from .tokens import CustomToken


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Кастомный серилизатор для вывода данных при обновлении токена
    """
    token_class = CustomToken
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')

        if attrs['refresh']:
            data = super().validate(attrs)
            data = {
                'tokens': data,
            }
            return data
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')


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

