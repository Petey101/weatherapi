from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('weather/', views.weather, name='weather'),
    path('update/', views.update, name='update'),
]
