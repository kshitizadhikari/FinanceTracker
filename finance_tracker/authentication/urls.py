from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import RegisterView, LoginView, ResetPasswordView, ResetUserPasswordView, VerificationView, UsernameValidationView, EmailValidationView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name="register"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('login', LoginView.as_view(), name="login"),
    path('reset-password', ResetPasswordView.as_view(), name="reset-password"),
    path('username-validation',csrf_exempt( UsernameValidationView.as_view()), name="username-validation"),
    path('email-validation',csrf_exempt( EmailValidationView.as_view()), name="email-validation"),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"),
    path('reset-user-password/<uidb64>/<token>', ResetUserPasswordView.as_view(), name="reset-user-password"),

]