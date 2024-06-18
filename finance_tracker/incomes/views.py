from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Source, Income
import json
from django.db.models import Q, F
from django.http import JsonResponse

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