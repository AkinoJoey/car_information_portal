from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car-details/', views.car_form, name='car-details'),
    path('testing/', views.testing, name="testing"),
    path('car_form/',views.car_form, name="car_form"),
    path('get-car-models',views.get_car_models, name='get-car-models'),
    path('your_backend_view',views.your_backend_view, name='your_backend_view')
]