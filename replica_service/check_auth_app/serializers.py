from rest_framework.serializers import ModelSerializer
from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "cqrs_revision",
            "user_permissions",
            "groups"
        ]
