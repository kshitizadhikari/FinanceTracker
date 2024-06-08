from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages

class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        form_username = request.POST['username']
        form_email = request.POST['email']
        form_password = request.POST['password']

        if len(form_password) < 6:
            messages.error(request, "Password Too Short")
        elif User.objects.filter(username=form_username).exists():
            messages.error(request, f"User already exists with the username {form_username}")
        elif User.objects.filter(email=form_email).exists():
            messages.error(request, f"User with {form_email} already exists")
        else:
            user = User.objects.create_user(
                username=form_username,
                email=form_email,
            )
            user.set_password(form_password)
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  # Redirect to a different page after successful registration
        
        return render(request, 'authentication/register.html')



class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        form_username = data['username']

        if not str(form_username).isalnum():
            return JsonResponse({
                "username_error": "Username should only contain letters and numbers",
            }, status=400)
        
        if User.objects.filter(username=form_username).exists():
            return JsonResponse({
                "username_error": "User with this username already exists",
            }, status=409)

        return JsonResponse({
            "username_valid": True
        })


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        form_email = data['email']

        if not validate_email(form_email):
            return JsonResponse({
                "email_error": "Invalid Email",
            }, status=400)
        
        if User.objects.filter(email=form_email).exists():
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
