from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import CarForm
from django.core.mail import send_mail
import requests
from django.http import JsonResponse
from django import forms
from .forms import *

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    return HttpResponse("this is a index page.")

def testing(request):
    return render(request, 'base.html')

@csrf_exempt
def get_car_models(request):
    if request.method == "POST":
        data = json.loads(request.body)
        models = create_car_models(data["makeId"])
        return JsonResponse(models,safe=False)
    
def car_form(request):
    context = {}
    if request.method == 'GET':
        form = CarForm()
        context['form'] = form
        return render(request, 'car_form.html', context)


# def car_form(request):
#     form = CarForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'car_form.html', context)
