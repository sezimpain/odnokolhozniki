from django.db.models import Avg
from rest_framework import serializers

from post.serializers import PostSerializer
from rating.views import RatingViewSet
from .models import Profile, Location
from friend import services as friend_services


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    is_follower = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source='username.username')

    class Meta:
        model = Profile
        fields = (
            'username',
            'bio',
            'name',
            'birth_date',
            'location',
            'gender',
            'total_followers',
            'total_following',
            'is_follower',
            'is_following'

        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['location'] = LocationSerializer(
            instance.location
        ).data
        action = self.context.get('action')
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
        if action == 'list':
            representation['followers'] = instance.followers.count()
            representation['following'] = instance.following.count()
            representation['posts'] = instance.posts.count()

        elif action == 'retrieve':
            representation['posts'] = PostSerializer(
                instance.posts.all(),
                many=True
            ).data
            representation['followers'] = instance.followers.all()
            representation['following'] = instance.following.all()

        return representation

    def get_is_follower(self, obj) -> bool:
        username = self.context.get('request').user
        return friend_services.is_follower(obj, username)

    def get_is_following(self, obj) -> bool:
        username = self.context.get('request').user
        return friend_services.is_following(obj, username)

    def create(self, validated_data):
        request = self.context.get('request')
        post = Profile.objects.create(username=request.user, **validated_data)
        return post

