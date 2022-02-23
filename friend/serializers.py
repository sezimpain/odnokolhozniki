from django.contrib.auth import get_user_model
from rest_framework import serializers

from friend.models import Follower
from friend.models import Following

User = get_user_model()


class FollowingSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_full_name(self, obj):
        return obj.get_full_name()

    def create(self, validated_data):
        username = self.context.get('request').user
        following = Follower.objects.create(
            username=username,
            **validated_data
        )
        return following


class FollowerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_full_name(self, obj):
        return obj.get_full_name()

    def create(self, validated_data):
        username = self.context.get('request').user
        follower = Following.objects.create(
            username=username,
            **validated_data
        )
        return follower

