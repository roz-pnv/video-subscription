from django.contrib import admin
from videos.models import Video
from videos.models import Actor
from videos.models import Director
from videos.models import Language
from videos.models import Category
from videos.models import Subscription
from videos.models import History
from videos.models import Rating

admin.site.register(Video)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(History)
admin.site.register(Rating)
