from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Source, Income
import json
from django.db.models import Q, F
from django.http import JsonResponse


def search_incomes(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText", "") 

        incomes = Income.objects.filter(
            Q(amount__startswith=search_str, owner=request.user) |
            Q(date__startswith=search_str, owner=request.user) |
            Q(description__icontains=search_str, owner=request.user) |
            Q(source__name__icontains=search_str, owner=request.user)
        ).annotate(source_name=F('source__name'))

        data = incomes.values('id', 'amount', 'date', 'description', 'source_name')

        return JsonResponse(list(data), safe=False)


@login_required(login_url='/auth/login')
def index(request):
    pageItemCount = 2
    incomes = Income.objects.filter(owner=request.user)
    paginator = Paginator(incomes, pageItemCount)
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
        'incomes': incomes,
        'page_obj': page_obj,
        'page_range': page_range
    }
    return render(request, 'incomes/index.html', context)

def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    
    if request.method == "POST":
        amount = request.POST["amount"]
        date = request.POST["date"]
        description = request.POST["description"]
        source_id = request.POST["source"]

        Income.objects.create(amount=amount, date=date, description=description, owner=request.user, source=Source.objects.get(pk=source_id))
        messages.success(request, "Income saved successfully")
        return redirect("income-index")
    return render(request, 'incomes/add_income.html', context)
    
def add_income_source(request):

    if request.method == "POST":
        name = request.POST["name"]
        Source.objects.create(name=name)
        messages.success(request, "Source saved successfully")
        return redirect("income-index")
    return render(request, 'incomes/add_source.html')

def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    if request.method == "POST":
        income.amount = request.POST['amount']
        income.date = request.POST['date']
        income.description = request.POST['description']
        # income.owner = request.user
        income.source = Source.objects.get(pk=request.POST['source'])
        income.save()
        return redirect('income-index')  # Redirect to some view after saving

    context = {
        'income': income,
        'sources': sources,
    }

    return render(request, 'incomes/edit_income.html', context) 


def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income deleted successfully")
    return redirect("income-index")