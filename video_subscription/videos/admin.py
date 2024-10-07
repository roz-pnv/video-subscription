from django.contrib import admin
from videos.models import Video
from videos.models import Actor
from videos.models import Director
from videos.models import Language
from videos.models import Category

admin.site.register(Video)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Language)
admin.site.register(Category)
