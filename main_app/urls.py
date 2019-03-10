from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.room, name='home'),
    path('lastMonthTH/', views.lastMonth),
    path('lastMonthPL/', views.lastMonth),
]
