from django.shortcuts import render
import pytz
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, 'home.html')


def users(request):
    mock_data = [
        {
            "id": 1,
            "full_name": "John Doe",
            "age": 30,
            "city": "New York",
        },
        {
            "id": 2,
            "full_name": "Jane Smith",
            "age": 25,
            "city": "Los Angeles",
        },
        {
            "id": 3,
            "full_name": "Mike Johnson",
            "age": 30,
            "city": "Chicago",
        },
        {
            "id": 4,
            "full_name": "Emily Brown",
            "age": 25,
            "city": "San Francisco",
        },
        {
            "id": 5,
            "full_name": "David Wilson",
            "age": 28,
            "city": "Seattle",
        },
    ]
    return render(request, 'users.html', {"users": mock_data})

def city_time(request):
    cities = {
        'Almaty': 'Asia/Almaty',
        'Calgary': 'America/Edmonton', 
        'Moscow': 'Europe/Moscow',
        'UTC': 'UTC'
    }
    
    if request.method == 'POST':
        selected_city = request.POST.get('city', 'UTC')
        timezone = cities.get(selected_city, 'UTC')
        
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        
        return render(request, 'city_time.html', {
            'cities': cities,
            'selected_city': selected_city,
            'current_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'timezone_name': timezone
        })
    
    return render(request, 'city_time.html', {'cities': cities})

def counter(request):
    if 'count' not in request.session:
        request.session['count'] = 0
    if request.method == 'POST':
        if 'increment' in request.POST:
            request.session['count'] += 1
        if 'reset' in request.POST:
            request.session['count'] = 0
    return render(request, 'counter.html', {'counter': request.session['count']})
