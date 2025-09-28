# messaging_app/urls.py
from django.contrib import admin
from django.urls import path, include
from chats import auth

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", auth.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", auth.TokenRefreshView.as_view(), name="token_refresh"),
    path("api/chats/", include("chats.urls")),
]
