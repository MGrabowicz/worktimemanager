# Generated by Django 3.2.9 on 2022-03-03 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('absenceType', models.CharField(choices=[('HOLIDAYP', 'Holiday paid'), ('HOLIDAYNP', 'Holiday not paid'), ('ONDEMAND', 'On demand')], default='HOLIDAYP', max_length=17)),
                ('workDays', models.IntegerField(blank=True, default=1, null=True)),
                ('manager', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='absenceManager', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='absenceOwner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
