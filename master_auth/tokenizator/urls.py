from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView
from .views import (CustomTokenObtainPairView,
                    CustomTokenRefreshView,
                    LogoutView,
                    LogoutAllView
                    )


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
]
