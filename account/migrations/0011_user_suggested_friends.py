# Generated by Django 5.0.1 on 2024-03-19 09:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_user_posts_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='suggested_friends',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
