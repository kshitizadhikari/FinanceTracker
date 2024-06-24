from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


# use /income/name when testing !!

urlpatterns = [
    path('', views.index, name="income-index"),
    path('add-income', views.add_income, name="add-income"),
    path('add-income-source', views.add_income_source, name="add-income-source"),
    path('edit-income/<int:id>', views.edit_income, name="edit-income"),
    path('delete-income/<int:id>', views.delete_income, name="delete-income"),
    path('search-incomes', csrf_exempt(views.search_incomes), name="search-incomes"),
    path('income-source-data', csrf_exempt(views.income_source_data), name="income-source-data"),
    path('income-summary', views.income_summary, name="income-summary")
]