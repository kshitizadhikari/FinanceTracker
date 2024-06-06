from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email


class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # Handle POST request for registration 
        pass


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({
                "username_error": "Username should only contain letters and numbers",
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "username_error": "User with this username already exists",
            }, status=409)

        return JsonResponse({
            "username_valid": True
        })


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({
                "email_error": "Invalid Email",
            }, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "email_error": "User with this email already exists",
            }, status=409)

        return JsonResponse({
            "email_valid": True
        })


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        # Handle POST request for login
        pass
