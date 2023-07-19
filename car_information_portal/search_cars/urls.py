from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('modelList/<str:make>/', views.model_list, name="model-list"),
    path('modelList/<str:make>/<str:model>/', views.model_data_list, name="model-data-list"),
    path('get-car-models',views.get_car_models, name='get-car-models'),
]