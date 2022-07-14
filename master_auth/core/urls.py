from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title='Auth Service Api',
        default_version='3.0.1',
        description="""Authentication service in microservice architecture. 
                    Support for database replication of user services.""",
        license=openapi.License(name='GNU License')
    ),
    public=True,
    permission_classes=[permissions.AllowAny,]
)


urlpatterns = [
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='api_doc'),
    path('admin/', admin.site.urls),
    path('auth/', include('tokenizator.urls'))
]
