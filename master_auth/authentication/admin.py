from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, UserGroup


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ("username", 'email', 'password', )}),
        ('Personal Info', {'fields': ("first_name", 'last_name')}),
        ('Statuses', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserGroup)
