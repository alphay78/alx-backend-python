from django.urls import path
from .views import delete_user

urlpatterns = [
   path("messaging/", include("messaging.urls")),
    path("delete-account/", delete_user, name="delete_user"),
]
