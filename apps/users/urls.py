from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/otp/setup/', views.otp_setup_view, name='otp_setup'),
    path('settings/otp/disable/', views.otp_disable_view, name='otp_disable'),
]
