from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car-details/', views.car_form, name='car-details'),
    path('testing/', views.testing, name="testing"),
]