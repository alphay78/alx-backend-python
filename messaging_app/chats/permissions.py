# chats/permissions.py
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object
    (message or conversation) to access it.
    Assumes the model has a `user` field pointing to the owner.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
