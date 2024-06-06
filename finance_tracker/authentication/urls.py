from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import RegisterView, LoginView, UsernameValidationView, EmailValidationView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('username-validation',csrf_exempt( UsernameValidationView.as_view()), name="username-validation"),
    path('email-validation',csrf_exempt( EmailValidationView.as_view()), name="email-validation"),
]