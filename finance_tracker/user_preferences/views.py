from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
import json
from django.conf import settings

# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    currency_list = []
    currency_file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    print(currency_file_path)
    with open(currency_file_path, "r") as f:
        try:
            data = json.load(f)
            for key, value in data.items():
                currency_list.append({
                    "name": key,
                    "value": value
                })
            print(currency_list)
        except json.JSONDecodeError:
            currency_list = []

    return render(request, 'userpreferences/index.html', {'currency_list': currency_list})