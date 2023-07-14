from django.shortcuts import render
from .forms import CarForm
from django.http import JsonResponse
from .forms import *
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
            make_id = make[0]
            make_display = make[1]
            makes.append({"make_id": make_id, "make_display": make_display, "format": ".webp"})
        context = {
            'request':request.method,
            'form': form,
            "makes": makes
        }
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            make = form.cleaned_data['make']
            original_model_name = form.cleaned_data['model']
            model_name = original_model_name.replace(" ", "%20")
        else:
            print(form.errors)
            
        car_data = get_car_data(make,model_name,int(request.POST['begin_year']),int(request.POST['end_year']))
        
        models = []
        for data in car_data:
            model_year = data[1]
            model_engine_power_ps = data[2]
            model_engine_cc = data[3]
            models.append({"model_year":model_year,"model_engine_power_ps":model_engine_power_ps,"model_engine_cc":model_engine_cc})
        
        context = {
            "request": request.method,
            "form": form,
            "make":make,
            "model_name":original_model_name,
            "models":models
        }
        
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
    
def model_list(request,make_name):
    print(request)
    form = CarForm({"make": make_name})
    context = {
            'form': form
        }
    return render(request, 'model_list.html',context)