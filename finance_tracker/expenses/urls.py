from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name="index"),
    path('add-expense', views.add_expense, name="add-expense"),
    path('add-expense-category', views.add_expense_category, name="add-expense-category"),
    path('edit-expense/<int:id>', views.edit_expense, name="edit-expense"),
    path('delete-expense<int:id>', views.delete_expense, name="delete-expense"),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search-expenses"),

]