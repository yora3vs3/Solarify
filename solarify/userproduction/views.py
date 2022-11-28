from django.shortcuts import render, redirect
from .models import Hybrid, UserProduction
from django.core.paginator import Paginator
from userpreferenses.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# Create your views here.


def search_production(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        production = UserProduction.objects.filter(
            power__istartswith=search_str, owner=request.user) | UserProduction.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserProduction.objects.filter(
            description__icontains=search_str, owner=request.user) | UserProduction.objects.filter(
            hybrid__icontains=search_str, owner=request.user)
        data = production.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Hybrid.objects.all()
    production = UserProduction.objects.filter(owner=request.user)
    paginator = Paginator(production, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'production': production,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'production/index.html', context)


@login_required(login_url='/authentication/login')
def add_production(request):
    Hybrid = Hybrid.objects.all()
    context = {
        'hybrid': Hybrid,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'production/add_production.html', context)

    if request.method == 'POST':
        power = request.POST['power']

        if not power:
            messages.error(request, 'power is required')
            return render(request, 'production/add_production.html', context)
        description = request.POST['description']
        date = request.POST['production_date']
        Hybrid = request.POST['Hybrid']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'production/add_production.html', context)

        UserProduction.objects.create(owner=request.user, power=power, date=date,
                                  Hybrid=Hybrid, description=description)
        messages.success(request, 'Record saved successfully')

        return redirect('production')


@login_required(login_url='/authentication/login')
def production_edit(request, id):
    production = UserProduction.objects.get(pk=id)
    hybrid = Hybrid.objects.all()
    context = {
        'production': production,
        'values': production,
        'hybrid': hybrid
    }
    if request.method == 'GET':
        return render(request, 'production/edit_production.html', context)
    if request.method == 'POST':
        power = request.POST['power']

        if not power:
            messages.error(request, 'power is required')
            return render(request, 'production/edit_production.html', context)
        description = request.POST['description']
        date = request.POST['production_date']
        Hybrid = request.POST['Hybrid']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'production/edit_production.html', context)
        production.power = power
        production. date = date
        production.Hybrid = Hybrid
        production.description = description

        production.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('production')


def delete_production(request, id):
    production = UserProduction.objects.get(pk=id)
    production.delete()
    messages.success(request, 'record removed')
    return redirect('production')
