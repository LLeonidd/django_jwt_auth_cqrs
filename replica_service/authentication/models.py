from django.db import models
from dj_cqrs.mixins import ReplicaMixin
from django.contrib.auth.models import AbstractUser, UserManager

from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _


class UserGroup(ReplicaMixin, models.Model):
    CQRS_ID = 'group'

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    def __str__(self):
        return self.name


class User(ReplicaMixin, AbstractUser):

    CQRS_ID = 'user'
    CQRS_CUSTOM_SERIALIZATION = True

    USER_GROUP_MODEL = UserGroup

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    # Поля модели, с отношением Many-to-Many, One-to-Mane
    # Для таких полей необходимо реализовавать функцию получения
    # связанных объектов и привязки к текущей модели.
    # В обработчиках событий, эти поля либо игнориуются, либо для них реализуется
    # функция получения связанных объектов.
    RELATION_FIELDS = ['groups', 'user_permissions']

    objects = UserManager()

    groups = models.ManyToManyField(
        USER_GROUP_MODEL,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )

    @staticmethod
    def _get_user_groups(mapped_data):
        groups_list = User.USER_GROUP_MODEL.objects.filter(pk__in=mapped_data)
        return groups_list

    @staticmethod
    def _delete_fields_map(mapped_data, fields):
        for field in fields:
            del mapped_data[field]
        return mapped_data

    @classmethod
    def cqrs_create(cls, sync, mapped_data, previous_data=None, meta=None):
        cls._delete_fields_map(mapped_data, User.RELATION_FIELDS)
        return cls.objects.create(**mapped_data)

    def cqrs_update(self, sync, mapped_data, previous_data=None, meta=None):
        related_groups = User._get_user_groups(mapped_data['groups'])

        User._delete_fields_map(mapped_data, User.RELATION_FIELDS)

        for key, value in mapped_data.items():
            setattr(self, key, value)

        self.groups.set(related_groups)
        self.save()
        return self

