from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.


def index(request):
    unit_data = []
    file_path = os.path.join(settings.BASE_DIR, 'units.json')
    
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            unit_data.append({'name': k, 'value': v})
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'units': unit_data,
                                                          'user_preferences': user_preferences})
    else:

        unit = request.POST['unit']
        if exists:
            user_preferences.unit = unit
            user_preferences.save()
        else:
            UserPreference.objects.create(user=request.user, unit=unit)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {'units': unit_data, 'user_preferences': user_preferences})
