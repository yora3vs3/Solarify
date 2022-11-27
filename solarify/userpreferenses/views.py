from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.


def index(request):
    Unit_data = []
    file_path = os.path.join(settings.BASE_DIR, 'Units.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            Unit_data.append({'name': k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'Units': Unit_data,
                                                          'user_preferences': user_preferences})
    else:

        Unit = request.POST['Unit']
        if exists:
            user_preferences.Unit = Unit
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, Unit=Unit)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'Units': Unit_data, 'user_preferences': user_preferences})
