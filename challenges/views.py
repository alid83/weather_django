from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from account_module.models import User, UserActivity
from datetime import date
from khayyam import JalaliDate


def convert_to_persian_date(myDate:str):
    Date = myDate.split('-')
    persian_date = JalaliDate(date(int(Date[0]), int(Date[1]), int(Date[2])))
    return persian_date


def api_weather(request):
    print("111")
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,is_day,wind_speed_10m&hourly=temperature_2m&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum&forecast_days=1'
        response = requests.get(url)
        data = response.json()
        sunrise = data["daily"]["sunrise"][0].split("T")
        sunset = data["daily"]["sunset"][0].split("T")
        max_temp = data["daily"]["temperature_2m_max"][0]
        min_temp = data["daily"]["temperature_2m_min"][0]
        current_temp = data["current"]["temperature_2m"]
        current_wind_speed = data["current"]["wind_speed_10m"]
        humidity = data["current"]["relative_humidity_2m"]
        is_day = data["current"]["is_day"]

        api_2 = f'https://api.api-ninjas.com/v1/reversegeocoding?lat={latitude}&lon={longitude}'
        response_2 = requests.get(api_2, headers={'X-Api-Key': 'r0PhcRuVj23Z0uN8Y5JSaA==jtUjqidNv2btUa7x'})
        dat = response_2.json()
        data = dict(dat[0])
        city = data['name']
        country = data['country']

        api_3 = f'https://api.api-ninjas.com/v1/country?name={country}'
        response_3 = requests.get(api_3, headers={'X-Api-Key': 'r0PhcRuVj23Z0uN8Y5JSaA==jtUjqidNv2btUa7x'})
        dat = response_3.json()
        data = dict(dat[0])
        capital = data['capital']
        continent = data['region'].split()[1]

        api_4 = f"http://worldtimeapi.org/api/timezone/{continent}/{capital}"
        response_4 = requests.get(api_4)
        dat = response_4.json()
        dateTime = dat['datetime'].split('T')
        t = dateTime[1].split(':')
        time = f'{t[0]}:{t[1]}'

        user: User = request.user
        full_name = user.get_full_name()
        user_activity: UserActivity = UserActivity.objects.filter(name__iexact=full_name).first()
        if user_activity.cities is not None:
            user_activity = UserActivity(
                user=user,
                name=user.get_full_name(),
                date_joined=user.date_joined,
                cities=city,
                date_search=dateTime[0],
                persian_date_search=convert_to_persian_date(dateTime[0])
            )
            user_activity.save()
        else:
            UserActivity.objects.filter(name__iexact=full_name).first().update(cities=city)

        return JsonResponse({
            'sunrise': sunrise,
            'sunset': sunset,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'current_temp': current_temp,
            'current_wind_speed': current_wind_speed,
            'humidity': humidity,
            'is_day': is_day,
            'city': city,
            'myTime': time,
        })


    return JsonResponse({'error': 'Invalid request'}, status=400)


def index(request):
    return render(request, 'challenges/indexPage.html')


def weather_Page(request):
    sesion_id = request.session.session_key
    if sesion_id is None:
       return redirect('login_page')

    user = User.objects.filter(id=request.user.id).first()
    return render(request, 'challenges/weather_page.html', {'name': user})
