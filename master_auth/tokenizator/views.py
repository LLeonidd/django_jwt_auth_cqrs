from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .tokens import CustomToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .serializers import CustomTokenRefreshSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Запрос токенов доступа и обновления. Токен обновления передается в COOKIES.
    """
    def finalize_response(self, request, response, *args, **kwargs):
        try:
            set_token_cookie(response)
        except InvalidToken:
            Response(status=status.HTTP_401_UNAUTHORIZED)

        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CustomTokenObtainPairSerializer


class CookieTokenRefreshView(TokenRefreshView):
    """
    Запрос обновления токенов. Токен обновления передается в COOKIES.
    """
    def finalize_response(self, request, response, *args, **kwargs):
        try:
            set_token_cookie(response)
        except InvalidToken:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    """
    Удаление токенов. Занесение токена обновления в черный список
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = CustomToken(refresh_token)
            token.blacklist()

            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie(key=settings.SIMPLE_JWT['AUTH_COOKIE_KEY'])

            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    """
    Занесение всех токенов выданных пользователю в черный список
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


def set_token_cookie(response):
    try:
        if response.data['tokens']['refresh']:
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_KEY'],
                value=response.data['tokens']['refresh'],
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                max_age=settings.SIMPLE_JWT['AUTH_COOKIE_MAX_AGE']
            )
            del response.data['tokens']['refresh']
    except KeyError:
        raise InvalidToken
