from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,\
    RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Room
from .permissions import IsOwnerProfileOrReadOnly
from .permissions import IsOwnerRoom
from .serializers import UserProfileSerializer
from .serializers import RoomSerializer


# class UserProfileListCreateView(ListCreateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class RoomCreateView(CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class RoomView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsOwnerRoom, IsAuthenticated]
