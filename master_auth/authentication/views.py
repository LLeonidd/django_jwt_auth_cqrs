from http import HTTPStatus
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class Validate(APIView):
    permission_classes = (IsAuthenticated,)
    # Отлавливаем валидацию на уровне пермишинов
    # Если токен валидный, то проверям что пользователь существует (не анонимный)

    def get(self, *a, **k):
        """
        Обработать get запрос валидации токена.
        """
        if self.request.user.id:
            # Если пользователь есть в системе
            return Response(status=HTTPStatus.OK)  # в ответе 200 статус
        else:
            # Если данного пользователя нет в системе
            return Response(status=HTTPStatus.UNAUTHORIZED)  # Во всех остальных случаях 401 статус


class UserView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.id)