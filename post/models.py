from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from like.models import Like
from post.tasks import notify_user


class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Post(Created):
    profile = models.ForeignKey(
        'profile_.Profile',
        related_name='posts',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True

    )
    caption = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    post = models.ImageField(
        upload_to='posts',
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])]
    )
    username = models.ForeignKey(
        'account.User',
        related_name='posts',
        on_delete=models.CASCADE
    )
    likes = GenericRelation(Like)
    #favorites = GenericRelation(Favorite)

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comments(self):
        return self.comments.count()

    class Meta:
        ordering = ('-created',)


@receiver(post_save, sender=Post)
def notify_about_creation(sender, instance, created, **kwargs):
    if created:
        notify_user.delay(instance.username.email)