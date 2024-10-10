from videos.models import Video
from videos.models import Subscription
from videos.models import Actor
from videos.models import Director
from videos.models import Language
from videos.models import Category
from videos.models import History
from videos.models import Rating
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils import timezone


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
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'name',
            'description',
            'video_url', 
            'is_subscription_needed', 
            'duration', 
            'languages', 
            'director', 
            'actors', 
            'categories', 
        ]
        read_only_fields = [
            'video_url', 
        ]
    
    
    actors = ActorSerializer(many=True, read_only=True, source='actors_id')
    languages = LanguageSerializer(many=True, read_only=True, source='languages_id')
    director = DirectorSerializer(read_only=True, source='director_id')
    categories = CategorySerializer(many=True, read_only=True, source='categories_id')
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
        read_only_fields = [
            'start_date', 
            'end_date', 
            'created_at',
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        subscription = Subscription.objects.create(
            type=validated_data.get('type', Subscription.TypeChoices.NORMAL),
            status=validated_data.get('status', Subscription.StatusChoices.DIACTIVE),
            start_date = timezone.now(),
            user_id=user
        )
        subscription.set_end_date()  
        subscription.save()
        return subscription


class RenewSubscriptionSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Subscription.TypeChoices.choices)
    status = serializers.ChoiceField(choices=Subscription.StatusChoices.choices)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.status = validated_data.get('status', instance.status)
        instance.renew()
        return 
    

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


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'id', 
            'video_id', 
            'user_id', 
            'score',
        ]
        read_only_fields = [
            'user_id', 
            'video_id', 
            'created_at',
        ]
