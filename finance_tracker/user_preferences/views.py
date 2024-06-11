from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages

@login_required(login_url='/auth/login')
def index(request):
    try:
        user_pref = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        user_pref = None

    if request.method == "POST":
        currency = request.POST["currency"]

        if user_pref:
            user_pref.currency = currency
            user_pref.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, "Currency saved successfully")

    #GET
    currency_list = []
    currency_file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(currency_file_path, "r") as f:
        try:
            data = json.load(f)
            for key, value in data.items():
                currency_list.append({
                    "name": key,
                    "value": value
                })
        except json.JSONDecodeError:
            currency_list = []

    return render(request, 'userpreferences/index.html', {
        'currency_list': currency_list,
        'user_pref': user_pref,
    })