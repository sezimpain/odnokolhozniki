from django.contrib import admin
from .models import Follower
from .models import Following
admin.site.register(Follower)
admin.site.register(Following)
