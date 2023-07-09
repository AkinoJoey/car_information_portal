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

@csrf_exempt
def get_car_models(request):
    if request.method == "POST":
        data = json.loads(request.body)
        models = create_car_models(data["makeId"])
        return JsonResponse(models,safe=False)

def index(request):
    if request.method == 'GET':
        form = CarForm()
        makes_tuple_list = get_car_makes()
        makes = []
        for make in makes_tuple_list:
            makes.append({"make_id": make[0], "make_display": make[1], "format": ".webp"})
        context = {
            'form': form,
            "makes": makes
        }
    if request.method == 'POST':
        form = CarForm(request.POST)
        context = {"form": form}
        car_data = get_car_data(request.POST['make'],request.POST['model'],int(request.POST['begin_year']),int(request.POST['end_year']))
        print(car_data)
        if form.is_valid():
            # return JsonResponse({"message": "Success"})
            print({"message": "Success"})
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors},status= 400)
        
    return render(request, 'index.html',context)

def testing(request):
    return render(request, 'base.html')


    
def car_form(request):
    if request.method == 'GET':
        form = CarForm()
        context = {
            'form': form
        }
        return render(request, 'car_form.html', context)
    



# def car_form(request):
#     form = CarForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'car_form.html', context)
