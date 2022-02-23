from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Follower, Following

User = get_user_model()


def add_following(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    following, is_created = Following.objects.get_or_create(
        content_type=obj_type,
        object_id=obj.id,
        user=user
    )
    '''follower, is_created = Follower.objects.get_or_create(
        content_type=obj_type,
        object_id=obj.id,
        user=user
    )'''

    return following #follower


def remove_following(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    Following.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user
    ).delete()
    '''Follower.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user
    ).delete()'''


def get_following(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        followers__content_type=obj_type,
        followers__object_id=obj.id
    )


def get_followers(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        following__content_type=obj_type,
        following__object_id=obj.id
    )


def is_follower(obj, user) -> bool:
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    following = Following.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user
    )
    return following.exists()


def is_following(obj, user) -> bool:
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    follower = Follower.objects.filter(
        content_type=obj_type,
        object_id=obj.id,
        user=user
    )
    return follower.exists()