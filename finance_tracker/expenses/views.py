from django.utils.dateparse import parse_date
import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
import json
from django.db.models import Q, F
from django.http import JsonResponse

@login_required(login_url='/auth/login')
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText", "") 

        expenses = Expense.objects.filter(
            Q(amount__startswith=search_str, owner=request.user) |
            Q(date__startswith=search_str, owner=request.user) |
            Q(description__icontains=search_str, owner=request.user) |
            Q(category__name__icontains=search_str, owner=request.user)
        ).annotate(category_name=F('category__name'))

        data = expenses.values('id', 'amount', 'date', 'description', 'category_name')

        return JsonResponse(list(data), safe=False)


@login_required(login_url='/auth/login')
def index(request):
    pageItemCount = 5
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, pageItemCount)
    page_num = 1
    if request.GET.get('page'):
        page_num = int(request.GET.get('page')) 
    page_obj = Paginator.get_page(paginator, page_num)
    page_obj = paginator.get_page(page_num)
    
    # Calculate the range of pages to display
    index = page_num - 1  # Current page index
    max_index = paginator.num_pages
    start_index = index - 1 if index >= 1 else index
    end_index = index + 2 if index <= max_index - 3 else max_index
    # Generate the page range to display
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'page_range': page_range
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/auth/login')
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

@login_required(login_url='/auth/login')
def add_expense_category(request):

    if request.method == "POST":
        name = request.POST["name"]
        Category.objects.create(name=name)
        messages.success(request, "Category saved successfully")
        return redirect("index")
    return render(request, 'expenses/add_category.html')

@login_required(login_url='/auth/login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
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


@login_required(login_url='/auth/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect("index")

@login_required(login_url='/auth/login')
def expense_category_data(request):

    # Initialize the expenses queryset
    expenses = Expense.objects.filter(owner=request.user)

    # Get today's date
    today_date = datetime.date.today()
    current_month_date = datetime.date(today_date.year, today_date.month, 1)

    # Get date_from and date_to from request and parse them
    date_from = parse_date(request.GET.get("date_from")) or current_month_date
    date_to = parse_date(request.GET.get("date_to")) or current_month_date


    # Apply date filters
    if date_from and date_to:
        expenses = expenses.filter(date__range=[date_from, date_to])
    elif date_from:
        expenses = expenses.filter(date__gte=date_from)
    elif date_to:
        expenses = expenses.filter(date__lte=date_to)

    
    final_report = {}

    def get_category_from_expense(expense):
        return expense.category
    
    category_list = list(set(map(get_category_from_expense, expenses)))

    def get_expense_from_category(category):
        expenses_from_category =  expenses.filter(category=category)
        amount = 0
        for item in expenses_from_category:
            amount += item.amount
        return amount

    for category in category_list:
        expense_from_category = get_expense_from_category(category)
        final_report[str(category)] = expense_from_category
    
    return JsonResponse(final_report,safe=False )


@login_required(login_url='/auth/login')
def expense_summary(request):
    return render(request, "expenses/expense_summary.html")
