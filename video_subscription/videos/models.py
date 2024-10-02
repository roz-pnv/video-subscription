from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Language(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Video(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=255)
    video_url = models.URLField(max_length=2048)
    duration = models.IntegerField()
    languages_id = models.ManyToManyField(Language)
    director_id = models.ManyToManyField(Director)
    actors_id = models.ManyToManyField(Actor)
    categories_id = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    class TypeChoices(models.TextChoices):
        NORMAL = 'NORMAL', 'Normal'
        ONE_MONTH = 'One_month', 'One month subscription'
        QUARTERLY  = 'Quarterly', 'Quarterly subscription'
        SIX_MONTH = 'Six_month', 'Six month subscription'
        ONE_YEAR = 'One_year', 'One year subscription'
        
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        DIACTIVE = 'DIACTIVE', 'diactive'

    type = models.CharField(
        max_length=23, 
        choices=TypeChoices.choices, 
        default=TypeChoices.NORMAL,
    )
    status = models.CharField(
        max_length=8, 
        choices=StatusChoices.choices, 
        default=StatusChoices.ACTIVE,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.end_date is None:
            if self.type == 'One_month':
                self.end_date = self.start_date + timedelta(days=30)
            elif self.type == 'Quarterly':
                self.end_date = self.start_date + timedelta(days=90)
            elif self.type == 'Six_month':
                self.end_date = self.start_date + timedelta(days=180)
            elif self.type == 'One_year':
                self.end_date = self.start_date + timedelta(days=360)
            self.end_date = None

        if self.end_date is None and self.end_date <= timezone.now():
            self.status = self.StatusChoices.DIACTIVE
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.type}: {self.status} ({self.start_date},{self.end_date})'


class History(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    video_id = models.ForeignKey(
        Video,
        on_delete=models.SET_NULL,
        null=True,
    )
    watch_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user_id} watch {self.video_id} at {self.watch_date}.'
