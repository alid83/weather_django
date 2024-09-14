from django.urls import path
from . import views


urlpatterns = [
    path('user_history/', views.UserHistory, name='user_history'),
    path('ajax_user_history/', views.ajax_user_history, name='ajax_user_history')
]