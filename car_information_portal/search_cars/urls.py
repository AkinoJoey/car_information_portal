from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('car-details/', views.car_form, name='car-details'),
    path('modelList/<str:make_name>/', views.model_list, name="model-list"),
    path('testing/', views.testing, name="testing"),
    path('car_form/',views.car_form, name="car_form"),
    path('get-car-models',views.get_car_models, name='get-car-models'),
]