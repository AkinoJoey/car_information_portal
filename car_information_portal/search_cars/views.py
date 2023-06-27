from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CarForm
from django.core.mail import send_mail
import requests
from django.http import JsonResponse
from django import forms

# Create your views here.
def index(request):
    return HttpResponse("this is a index page.")

def testing(request):
    return render(request, 'base.html')

# def car_form(request):
#     form = CarForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'car_maker.html', context)

from .forms import CarForm

def car_form(request):
    form = CarForm()
    return render(request, 'car_maker.html', {'form': form})

def get_models(request):
    make_id = request.GET.get('make_id')
    url = f'https://www.carqueryapi.com/api/0.3/?cmd=getModels&make={make_id}'
    headers = {'User-Agent': 'Chrome/114.0'}
    response = requests.get(url)
    data = response.json()
    models = [(model['model_name'], model['model_name']) for model in data['Models']]
    print(url)
    print('test')
    return JsonResponse({'models': models})