from django.db import models

class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Content(Created):
    image = models.ImageField(upload_to='content')
    description = models.TextField()
    author = models.ForeignKey('account.User', related_name='content')
    def __str__(self):
        return f"{self.title} -> Author:{self.author.email}"

class Image(Created):
    image = models.ImageField(upload_to='images', null=False, blank=False)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='images')

