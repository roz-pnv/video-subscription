from videos.models import Video
from videos.models import Subscription
from django.contrib.auth.models import User

from rest_framework import serializers

from rest_framework import serializers
from .models import Actor, Director, Language, Category, Video

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    works = serializers.StringRelatedField(many=True)
    class Meta:
        model = Director
        fields = [
            'first_name',
            'last_name',
            'works',
        ]

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    # languages = LanguageSerializer(many=True, read_only=True)
    # categories = CategorySerializer(many=True, read_only=True)
    # actor = ActorSerializer(many=True, read_only=True)
    # works = DirectorSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = [
            'name',
            'description',
            'video_url', 
            'is_subscription_needed', 
            'duration', 
            'languages_id', 
            'director_id', 
            'actors_id', 
            'categories_id', 
        ]
    
    video_url = serializers.SerializerMethodField()

    def get_video_url(self, obj):
        request = self.context.get('request')
        user = request.user

        
        if not user.is_authenticated:
            return 'You need to purchase a subscription to view the video.'

        if user.is_staff:
            return obj.video_url

        if obj.is_subscription_needed:
            has_active_subscription = Subscription.objects.filter(
                user_id=user, 
                status=Subscription.StatusChoices.ACTIVE
            )
            print(has_active_subscription)
            if has_active_subscription.exists():
                return obj.video_url
            else:
                return 'You need to purchase a subscription to view the video.'
        
        return obj.video_url

