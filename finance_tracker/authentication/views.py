from django.contrib.auth.tokens import PasswordResetTokenGenerator
from threading import Thread
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.views import View
from .utils import token_generator
from django.contrib import auth
import json
import os
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site

# EMAIL THREAD 
class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self) -> None:
        self.email.send(fail_silently=False)  

class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        form_username = request.POST['username']
        form_email = request.POST['email']
        form_password = request.POST['password']

        if len(form_password) < 8:
            messages.error(request, "Password Too Short")
        elif User.objects.filter(username=form_username).exists():
            messages.error(request, f"User already exists with the username {form_username}")
        elif User.objects.filter(email=form_email).exists():
            messages.error(request, f"User with {form_email} already exists")
        else:
            user = User.objects.create_user(
                username=form_username,
                email=form_email,
                is_active=False
            )
            user.set_password(form_password)
            user.save()
            

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = "http://" + domain + link

            # send register email
            email_subject = 'Welcome to Finance Tracker'
            email_body = f"Dear {user.username}, your account has been created successfully\n Please use the below link to activate your account:\n{activate_url}"
            email_from = 'noreply@semycolon.com'
            recipient_list = [user.email]

            email = EmailMessage(
                email_subject,
                email_body,
                email_from,
                recipient_list
            )
            EmailThread(email).start()
            messages.success(request, "Account created successfully. A mail has been sent to the registered email. Please use that to activate the account !")
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
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, "Please fill all fields")
            return redirect('login')
        
        user = auth.authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                messages.info(request, "Please activate your account using the link in your email")
                return redirect('login')
            auth.login(request, user)
            messages.success(request, "You have been successfully logged in")
            # redirect to the index route of expenses app url
            return redirect('index')  
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')



class VerificationView(View):

    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if token_generator.check_token(user, token):
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(request, "Account activated successfully.")
                else:
                    messages.info(request, "Account has already been activated.")
            else:
                messages.error(request, "Invalid activation link or account already activated.")

        except User.DoesNotExist:
            messages.error(request, "Invalid activation link.")
        except Exception as ex:
            messages.error(request, "An error occurred during account activation.")

        return redirect('login')


class LogoutView(View):
    def get(self, request):
        storage = messages.get_messages(request)
        for _ in storage:
            pass
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return redirect('login')
    

class ResetPasswordView(View):
    def get(self, request):
        return render(request, "authentication/reset-password.html")


    def post(self, request):
        form_email = request.POST.get("email")

        context = {
            'values': request.POST
        }

        if not validate_email(form_email):
            messages.error(request, "Invalid Email")
            return render(request, "authentication/reset-password.html", context)

        try:
            user = User.objects.get(email=form_email)
        except User.DoesNotExist:
            messages.error(request, f"User with email {form_email} doesn't exist")
            return render(request, "authentication/reset-password.html", context)
        
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        token = PasswordResetTokenGenerator().make_token(user)
        link = reverse('reset-user-password', kwargs={'uidb64': uidb64, 'token': token})
        password_reset_url = f"http://{domain}{link}"

        # send reset email
        email_subject = 'Finance Tracker Password Reset'
        email_body = f"Dear {user.username},\n\nPlease use the link below to reset your password:\n{password_reset_url}"
        email_from = 'noreply@semycolon.com'
        recipient_list = [user.email]

        reset_email = EmailMessage(
            email_subject,
            email_body,
            email_from,
            recipient_list
        )
        EmailThread(reset_email).start()

        messages.success(request, "We have sent you an email to reset your password")
        return redirect("index")

class ResetUserPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, "authentication/set-new-password.html", context)
    
    def post(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        old_password = request.POST.get("oldPassword")
        if not auth.authenticate(username=user.username, password=old_password):
            messages.error(request, "Password doesn't match current password")
            return redirect("reset-user-password", uidb64, token)
        
        new_password = request.POST.get("newPassword")
        user.set_password(new_password)
        user.save()
        messages.success(request, "Your new password has been set successfully")
        return redirect("login")
