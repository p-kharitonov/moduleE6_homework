from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView,\
    RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Account, Room, Message
from .permissions import IsOwnerAccountOrReadOnly
from .permissions import IsOwnerRoom
from .permissions import IsJoinedToRoom
from .serializers import AccountSerializer
from .serializers import RoomSerializer
from .serializers import RoomJoinSerializer
from .serializers import MessageSerializer


# class AccountListCreateView(ListCreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(user=user)


class AccountDetailView(RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerAccountOrReadOnly, IsAuthenticated]

    def get_object(self):
        return Account.objects.get(user=self.request.user)


class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class RoomCreateView(CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class RoomChangeView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsOwnerRoom, IsAuthenticated]


class RoomJoinView(UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomJoinSerializer
    permission_classes = [IsAuthenticated]


class MessageListView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsJoinedToRoom, IsAuthenticated]
    paginate_by = 100

    def get_queryset(self):
        try:
            room = Room.objects.get(pk=self.kwargs['pk'])
            return Message.objects.filter(room=room)
        except:
            return None

