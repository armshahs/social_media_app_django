# -*- coding: utf-8 -*-

import django
import sys
import os


from datetime import timedelta
from collections import Counter
from django.utils import timezone


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Social_Media.settings")
django.setup()

from account.models import User


users = User.objects.all()

for user in users:
    # Clear the suggestion list
    user.suggested_friends.clear()

    print("Find friends for:", user)

    for friend in user.friends.all():
        print("Is friend with:", friend)

        for friendsfriend in friend.friends.all():
            if friendsfriend not in user.friends.all() and friendsfriend != user:
                user.suggested_friends.add(friendsfriend)

    print()
