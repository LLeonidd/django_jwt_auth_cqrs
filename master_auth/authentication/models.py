from django.db import models
from dj_cqrs.mixins import MasterMixin
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import (
    AbstractUser, UserManager, Permission
)


class UserGroup(MasterMixin, models.Model):
    CQRS_ID = 'group'
    CQRS_PRODUCE = True

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    def __str__(self):
        return self.name


class User(AbstractUser, MasterMixin):

    CQRS_ID = 'user'
    CQRS_PRODUCE = True
    CQRS_SERIALIZER = 'authentication.serializers.UserSerializer'

    USER_GROUP_MODEL = UserGroup

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

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

    @classmethod
    def relate_cqrs_serialization(cls, queryset):
        return queryset.prefetch_related('groups')

