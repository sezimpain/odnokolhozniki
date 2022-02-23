from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from friend.models import Follower, Following


Gender = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]


class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Location(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    location = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.location


class Profile(Created):
    bio = models.CharField(
        max_length=255,
        blank=True
    )
    name = models.CharField(
        max_length=30,
        unique=True
    )
    username = models.ForeignKey(
        'account.User',
        related_name='profiles',
        on_delete=models.CASCADE
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='profiles'
    )
    gender = models.CharField(
        max_length=15,
        choices=Gender,
        default="Female"
    )
    followers = GenericRelation(Follower)
    following = GenericRelation(Following)

    @property
    def total_posts(self):
        return self.posts.count()

    @property
    def total_followers(self):
        return self.followers.count()

    @property
    def total_following(self):
        return self.following.count()




'''class Follower(models.Model):
    username = models.ForeignKey(
        'account.User',
        related_name='profiles',
        on_delete=models.CASCADE
    )'''
