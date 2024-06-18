from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="income-index"),
    path('add-income', views.add_income, name="add-income"),
]