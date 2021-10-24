from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Room


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')
        # fields = '__all__'
        read_only_fields = ('username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = ('user', 'room', 'avatar',)
        # fields = '__all__'

    def update(self, instance, validated_data, partial=True):
        if 'user' in validated_data:
            user = instance.user
            profile_user = validated_data.pop('user')
            user.first_name = profile_user.get('first_name', user.first_name)
            user.last_name = profile_user.get('last_name', user.last_name)
            user.save()
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'description', 'created_at']
        read_only_fields = ('created_at',)
