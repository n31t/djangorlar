from typing import Any, Dict, Tuple
from datetime import datetime
import pytz

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import User


def welcome_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'welcome.html')


def users_view(request: HttpRequest) -> HttpResponse:
    if User.objects.count() == 0:
        sample_users = [
            User(full_name="Айдос Ермеков", age=25, email="aidos@example.com"),
            User(full_name="Жанар Куанышбаева", age=30, email="janar@example.com"),
            User(full_name="Алихан Тлеуберген", age=28, email="alikhan@example.com"),
            User(full_name="Бекзат Нурланов", age=35, email="bekzat@example.com"),
            User(full_name="Айсулу Сагындыкова", age=22, email="aisulu@example.com"),
        ]
        User.objects.bulk_create(sample_users)
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def city_time_view(request: HttpRequest) -> HttpResponse:
    """Display real-time for selected cities"""
    cities = {
        'Almaty': 'Asia/Almaty',
        'Calgary': 'America/Denver',  
        'Moscow': 'Europe/Moscow',
        'UTC': 'UTC',
    }
    
    selected_city = request.GET.get('city', 'UTC')
    if selected_city not in cities:
        selected_city = 'UTC'
    
    try:
        if selected_city == 'UTC':
            timezone = pytz.UTC
        else:
            timezone = pytz.timezone(cities[selected_city])
        current_time = datetime.now(timezone)
    except Exception:
        timezone = pytz.UTC
        current_time = datetime.now(timezone)
        selected_city = 'UTC'
    context = {
        'cities': cities,
        'selected_city': selected_city,
        'current_time': current_time,
    }
    return render(request, 'city_time.html', context)


def counter_view(request: HttpRequest) -> HttpResponse:
    if 'counter' not in request.session:
        request.session['counter'] = 0
    
    return render(request, 'counter.html', {'counter': request.session['counter']})


@csrf_exempt
@require_http_methods(["POST"])
def counter_increment(request: HttpRequest) -> JsonResponse:
    if 'counter' not in request.session:
        request.session['counter'] = 0
    
    request.session['counter'] += 1
    request.session.save()
    
    return JsonResponse({'counter': request.session['counter']})

@csrf_exempt  
@require_http_methods(["POST"])
def counter_reset(request: HttpRequest) -> JsonResponse:
    request.session['counter'] = 0
    request.session.save()
    
    return JsonResponse({'counter': request.session['counter']})


def get_time_api(request: HttpRequest) -> JsonResponse:
    cities = {
        'Almaty': 'Asia/Almaty',
        'Calgary': 'America/Denver',  
        'Moscow': 'Europe/Moscow',
        'UTC': 'UTC',
    }
    
    selected_city = request.GET.get('city', 'UTC')
    if selected_city not in cities:
        selected_city = 'UTC'
    
    try:
        if selected_city == 'UTC':
            timezone = pytz.UTC
        else:
            timezone = pytz.timezone(cities[selected_city])
        current_time = datetime.now(timezone)
    except Exception:
        timezone = pytz.UTC
        current_time = datetime.now(timezone)
        selected_city = 'UTC'
    return JsonResponse({
        'city': selected_city,
        'time': current_time.strftime('%H:%M:%S'),
        'date': current_time.strftime('%Y-%m-%d'),
        'full_datetime': current_time.isoformat()
    })

def hello_name_view(
    _: HttpRequest,
    *args: Tuple[Any, ...],
    **kwargs: Dict[str, Any],
) -> HttpResponse:
    return render(
        request=_,
        template_name="index.html",
        context={
            "name" : "Amir",
            "names" : [],
        },
        status=200,
    )