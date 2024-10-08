import django_filters
from videos.models import Video

class VideoFilter(django_filters.FilterSet):
    language_name = django_filters.CharFilter(field_name='languages__name', lookup_expr='icontains')
    category_name = django_filters.CharFilter(field_name='categories__name', lookup_expr='icontains')

    class Meta:
        model = Video
        fields = ['language_name', 'category_name']
