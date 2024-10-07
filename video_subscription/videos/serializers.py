from videos.models import Video
from videos.models import Subscription
from videos.models import Actor
from videos.models import Director
from videos.models import Language
from videos.models import Category
from videos.models import History
from django.contrib.auth.models import User
from rest_framework import serializers


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
                user_id=user.id, 
                status=Subscription.StatusChoices.ACTIVE,
                type__in=[
                    Subscription.TypeChoices.ONE_MONTH,
                    Subscription.TypeChoices.QUARTERLY,
                    Subscription.TypeChoices.SIX_MONTH,
                    Subscription.TypeChoices.ONE_YEAR
                ],
            ).exists()
            if has_active_subscription:

                return obj.video_url
            else:
                return 'You need to purchase a subscription to view the video.'
        
        return obj.video_url


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id', 
            'type', 
            'status', 
            'start_date', 
            'end_date', 
            'created_at',
        ]

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = [
            'user_id', 
            'video_id', 
            'video_name', 
            'rating', 
            'watch_date',
        ]

    video_name = serializers.CharField(
        source='video_id.name', 
        read_only=True,
    )


