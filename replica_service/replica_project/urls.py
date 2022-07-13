from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('check_auth/', include('check_auth_app.urls')),
]
