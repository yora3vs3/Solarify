from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Usage
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferenses.models import UserPreference
import datetime


def search_usage(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        usage=""
        usage =  Usage.objects.filter(
            power__istartswith=search_str, owner=request.user) | Usage.objects.filter(
            date__istartswith=search_str, owner=request.user) | Usage.objects.filter(
            description__icontains=search_str, owner=request.user) | Usage.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = usage.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    usage = Usage.objects.filter(owner=request.user)
    paginator = Paginator(usage, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    units = UserPreference.objects.get(user=request.user).units
    context = {
        'usage': usage,
        'page_obj': page_obj,
        'units': units
    }
    return render(request, 'usage/index.html', context)


@login_required(login_url='/authentication/login')
def add_usage(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'usage/add_usage.html', context)

    if request.method == 'POST':
        power = request.POST['power']

        if not power:
            messages.error(request, 'power is required')
            return render(request, 'usage/add_usage.html', context)
        description = request.POST['description']
        date = request.POST['usage_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'usage/add_usage.html', context)

        Usage.objects.create(owner=request.user, power=power, date=date,
                               category=category, description=description)
        messages.success(request, 'usage saved successfully')

        return redirect('usage')


@login_required(login_url='/authentication/login')
def usage_edit(request, id):
    usage = Usage.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'usage': usage,
        'values': usage,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'usage/edit-usage.html', context)
    if request.method == 'POST':
        power = request.POST['power']

        if not power:
            messages.error(request, 'power is required')
            return render(request, 'usage/edit-usage.html', context)
        description = request.POST['description']
        date = request.POST['usage_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'usage/edit-usage.html', context)

        usage.owner = request.user
        usage.power = power
        usage. date = date
        usage.category = category
        usage.description = description

        usage.save()
        messages.success(request, 'usage updated  successfully')

        return redirect('usage')


def delete_usage(request, id):
    usage = Usage.objects.get(pk=id)
    usage.delete()
    messages.success(request, 'usage removed')
    return redirect('usage')


def usage_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    usage = Usage.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(usage):
        return usage.category
    category_list = list(set(map(get_category, usage)))

    def get_usage_category_power(category):
        power = 0
        filtered_by_category = usage.filter(category=category)

        for item in filtered_by_category:
            power += item.power
        return power

    for x in usage:
        for y in category_list:
            finalrep[y] = get_usage_category_power(y)

    return JsonResponse({'usage_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'usage/stats.html')
