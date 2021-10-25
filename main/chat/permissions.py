from rest_framework.permissions import BasePermission,SAFE_METHODS
from .models import Room, UserProfile


class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerRoom(BasePermission):
    def has_object_permission(self, request, view, obj):
        profile_user = UserProfile.objects.get(user=request.user)
        room = Room.objects.get(pk=obj.pk)
        if request.method in SAFE_METHODS:
            return True
        return room.own == profile_user
