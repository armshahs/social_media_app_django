# Generated by Django 5.0.1 on 2024-03-13 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_friends_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='friendrequest',
            options={'ordering': ('-created_at',)},
        ),
    ]
