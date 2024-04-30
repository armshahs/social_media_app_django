from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from account.models import User


# Create your views here.
def activateemail(request):
    email = request.GET.get("email", "")
    id = request.GET.get("id", "")

    if email and id:
        user = User.objects.get(id=id, email=email)
        print(user)
        user.is_active = True
        user.save()
        # cannot use Response from rest framework as you have not used @api_view decorator. This is a pure function
        return JsonResponse({"message": "account activated"})
    return JsonResponse({"message": "Activation failed"})
