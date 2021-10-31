from rest_framework import serializers
from chat.models import Account
from chat.models import Room
from chat.models import Message
from rest_framework import status
from rest_framework.response import Response


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', max_length=150)
    last_name = serializers.CharField(source='user.last_name', max_length=150)
    email = serializers.CharField(source='user.email', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True,
                                            format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Account
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'avatar')
        read_only_fields = ('id', 'username', 'date_joined', 'created_at')
        # fields = '__all__'

    def update(self, instance, validated_data, partial=True):
        if 'user' in validated_data:
            user = instance.user
            account = validated_data.pop('user')
            user.first_name = account.get('first_name', user.first_name)
            user.last_name = account.get('last_name', user.last_name)
            user.save()
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    author = AccountSerializer(read_only=True)
    members = AccountSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Room
        fields = ('id', 'title', 'get_absolute_url', 'description', 'author', 'members', 'created_at')
        read_only_fields = ('id', 'author', 'members', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        account = Account.objects.get(user=user)
        room = Room.objects.create(author=account, **validated_data)
        room.members.add(account)
        return room


class RoomJoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('id',)

    def update(self, instance, validated_data, partial=True):
        user = self.context['request'].user
        account = Account.objects.get(user=user)
        if instance.members.filter(pk=account.pk).exists():

            return instance
        else:
            instance.members.add(account)
            return instance


class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    author = serializers.CharField()

    class Meta:
        model = Message
        fields = ('created_at', 'author', 'content')
