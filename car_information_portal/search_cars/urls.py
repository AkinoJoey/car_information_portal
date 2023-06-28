from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car-details/', views.car_form, name='car-details'),
    path('testing/', views.testing, name="testing"),
    # path('car/',views.car_list, name='car_list'),
    # path('car/models/', views.get_models, name='get_models'),
    path('form/',views.car_form, name="car_form")
]