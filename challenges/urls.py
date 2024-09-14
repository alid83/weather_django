from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('weather/', views.weather_Page, name='weather'),
    path('api_weather/', views.api_weather, name='api_weather'),
]