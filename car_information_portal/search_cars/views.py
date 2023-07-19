from django.shortcuts import render
from .forms import CarForm
from django.http import JsonResponse
from . import forms
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from django.http import Http404

@csrf_exempt
def get_car_models(request):
    if request.method == "GET":
        raise Http404
    
    if request.method == "POST":
        data = json.loads(request.body)
        models = forms.create_car_models(data["makeId"])
        return JsonResponse(models,safe=False)
    
def create_model_details_list(make_id,model_name,begin_year,end_year):
    car_data = forms.get_car_data(make_id,model_name,begin_year,end_year)
    models = []
    
    for data in car_data:
        model_year = data[1]
        model_engine_power_ps = data[2]
        model_engine_cc = data[3]
        models.append({"model_year":model_year,"model_engine_power_ps":model_engine_power_ps,"model_engine_cc":model_engine_cc})
    
    return models
    
def create_display_data_context(request):
    form = CarForm(request.POST)
    form.set_model_choices(request.POST.get('make'))
    
    if form.is_valid():
        make_id = form.cleaned_data['make']
        original_model_name = form.cleaned_data['model']
        model_name = original_model_name.replace(" ", "%20")
    else:
        print(form.errors)
    
    models = create_model_details_list(make_id,model_name,int(request.POST['begin_year']),int(request.POST['end_year']))
    make_display = form.get_make_display(make_id)
    context = {
        "request": request.method,
        "form": form,
        "model_name":original_model_name,
        "make":make_display,
        "models":models
    }
    
    return context

def index(request):
    if request.method == 'GET':
        form = CarForm()
        makes_tuple_list = forms.get_car_makes()
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
        context = create_display_data_context(request)
        
    return render(request, 'index.html',context)
    
def model_list(request,make):
    if request.method == 'GET':
        form = CarForm(initial={"make":make})
        make_display =  form.get_make_display(make)
        
        if make_display is None:
            raise Http404
        
        form.set_model_choices(make)
        current_year = date.today().year
        # 2023のモデルリストがないからとりあえず2005にしておく
        models = forms.create_car_models_by_year(make,2005)
        context = {
                'request':request.method,
                'form': form,
                'make_id': make,
                'make_display': make_display,
                "format": ".webp",
                'current_year': current_year,
                'models':models
            }
        
    if request.method == 'POST':
        context = create_display_data_context(request)
        
    return render(request, 'model_list.html',context)

def model_data_list(request,make,model):
    if request.method == 'GET': 
        begin_year = forms.get_min_year()
        end_year = forms.get_max_year()
        
        initial = {
            'request':request.method,
            'make':make,
            'begin_year':begin_year,
            'end_year':end_year
        }
        
        form = CarForm(initial=initial)
        make_display =  form.get_make_display(make)
        
        if make_display is None:
            return render(request, '404.html')
        
        form.set_model_choices(make)
        form.set_model_initial(model)
        models = create_model_details_list(make,model,int(begin_year),int(end_year))
        if len(models) == 0:
            raise Http404
        context = {
            'request':request.method,
            'form':form,
            'make':make_display,
            'model_name':model,
            'models':models
        }
        
    if request.method == 'POST':
        context = create_display_data_context(request)
        
    return render(request,'model_data_list.html',context)