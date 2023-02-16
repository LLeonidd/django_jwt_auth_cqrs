from django.urls import path
from .views import (
                    LogoutView,
                    LogoutAllView,
                    )
from .views import CookieTokenObtainPairView, CookieTokenRefreshView
from authentication.views import Validate


urlpatterns = [
    path('login/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
    path('validate/', Validate.as_view(), name='val'),
]
