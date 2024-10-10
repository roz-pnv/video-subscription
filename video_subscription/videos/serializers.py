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
from django.db.models import Avg


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
            'average_rating',
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
            'average_rating',
        ]
    
    average_rating = serializers.SerializerMethodField()
    actors = ActorSerializer(Actor.objects.all(), many=True, source='actors_id')
    languages = LanguageSerializer(Language.objects.all(), many=True, source='languages_id')
    director = DirectorSerializer(Director.objects.all(), source='director_id')
    categories = CategorySerializer(Category.objects.all(), many=True, source='categories_id')
    video_url = serializers.SerializerMethodField()

    
    # def create(self, validated_data):
    #     actors_data = validated_data.pop('actors', [])
    #     categories_data = validated_data.pop('categories', [])
    #     languages_data = validated_data.pop('languages', [])
        
    #     video = Video.objects.create(**validated_data)
        
    #     for actor_data in actors_data:
    #         actor, created = Actor.objects.get_or_create(**actor_data)
    #         video.actors_id.add(actor)
        
    #     for category_data in categories_data:
    #         category, created = Category.objects.get_or_create(**category_data)
    #         video.categories_id.add(category)

    #     for language_data in languages_data:
    #         language, created = Language.objects.get_or_create(**language_data)
    #         video.languages_id.add(language)
        
    #     video.save()
    #     return video
    

    # def update(self, instance, validated_data):
    #     actors_data = validated_data.pop('actors', [])
    #     categories_data = validated_data.pop('categories', [])
    #     languages_data = validated_data.pop('languages', [])

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     instance.actors.clear()
    #     for actor_data in actors_data:
    #         actor, created = Actor.objects.get_or_create(**actor_data)
    #         instance.actors_id.add(actor)

    #     instance.categories.clear()
    #     for category_data in categories_data:
    #         category, created = Category.objects.get_or_create(**category_data)
    #         instance.categories_id.add(category)

    #     instance.languages.clear()
    #     for language_data in languages_data:
    #         language, created = Language.objects.get_or_create(**language_data)
    #         instance.languages_id.add(language)


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
    

    def get_average_rating(self, obj):
        avg_rating = obj.ratings.aggregate(Avg('score'))['score__avg']
        return avg_rating if avg_rating is not None else 0 


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
