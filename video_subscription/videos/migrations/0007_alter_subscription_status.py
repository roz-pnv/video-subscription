# Generated by Django 5.1.1 on 2024-10-07 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_alter_history_watch_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('DIACTIVE', 'diactive')], default='ACTIVE', max_length=8),
        ),
    ]
