from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expense

@login_required(login_url='/auth/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
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
        category_id = request.POST["category"]

        Expense.objects.create(amount=amount, date=date, description=description, owner=request.user, category=Category.objects.get(pk=category_id))
        messages.success(request, "Expense saved successfully")
        return redirect("index")
    return render(request, 'expenses/add_expense.html', context)


def add_expense_category(request):

    if request.method == "POST":
        name = request.POST["name"]
        Category.objects.create(name=name)
        messages.success(request, "Category saved successfully")
        return redirect("index")
    return render(request, 'expenses/add_category.html')


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    print(expense.category)
    if request.method == "POST":
        expense.amount = request.POST['amount']
        expense.date = request.POST['date']
        expense.description = request.POST['description']
        # expense.owner = request.user
        expense.category = Category.objects.get(pk=request.POST['category'])
        expense.save()
        return redirect('index')  # Redirect to some view after saving

    context = {
        'expense': expense,
        'categories': categories,
    }

    return render(request, 'expenses/edit_expense.html', context)

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect("index")