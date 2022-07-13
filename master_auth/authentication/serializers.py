from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField
from .models import User, UserGroup


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(ModelSerializer):

    class Meta:
        model = UserGroup
        fields = '__all__'


