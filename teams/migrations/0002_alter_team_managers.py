# Generated by Django 3.2.9 on 2022-03-03 16:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='managers',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='managers', to=settings.AUTH_USER_MODEL),
        ),
    ]
