# Generated by Django 5.0.1 on 2024-03-13 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_friends_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends_count',
            field=models.IntegerField(default=0),
        ),
    ]
