from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Room, Account


class IsOwnerAccountOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsOwnerRoom(BasePermission):
    def has_object_permission(self, request, view, obj):
        account = Account.objects.get(user=request.user)
        room = Room.objects.get(pk=obj.pk)
        if request.method in SAFE_METHODS:
            return True
        return room.author == account


class IsJoinedToRoom(BasePermission):
    def has_permission(self, request, view):
        try:
            pk = view.kwargs.get('pk', None)
            account = Account.objects.get(user=request.user)
            room = Room.objects.get(pk=pk)
            print(room)
            if request.method in SAFE_METHODS:
                return True
            return room.members.filter(pk=account.pk).exists()
        except:
            return False

