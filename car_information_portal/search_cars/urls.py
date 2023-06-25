from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.get_name, name='get_name'),
    path('car-details/', views.get_car_details, name='car-details'),
    path('testing/', views.testing, name="testing")
]