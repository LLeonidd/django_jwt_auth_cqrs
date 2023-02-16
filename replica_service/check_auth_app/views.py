from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from authentication.models import User
from .serializers import UserSerializer


class UserView(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.id)

