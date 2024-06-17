from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expense

@login_required(login_url='/auth/login')
def index(request):
    expenses = Expense.objects.all()
    context = {
        'expenses': expenses
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    

    if request.method == "POST":
        amount = request.POST["amount"]
        date = request.POST["date"]
        description = request.POST["description"]
        category = request.POST["category"]

        Expense.objects.create(amount=amount, date=date, description=description, owner=request.user, category=category)
        messages.success(request, "Expense saved successfully")

    return render(request, 'expenses/add_expense.html', context)