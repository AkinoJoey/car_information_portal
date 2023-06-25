from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import NameForm
from django.core.mail import send_mail
import requests
from django.http import JsonResponse

# Create your views here.
def index(request):
    return HttpResponse("this is a index page.")

def get_name(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/thanks/")
    else:
        form = NameForm()
        return render(request, "name.html", {"form": form})
    

def testing(request):
    return render(request, 'base.html')

def get_car_details(request):
    api_url = "https://www.carqueryapi.com/api/0.3/"
    make = request.GET.get("make")
    model = request.GET.get("model")

    response = requests.get(f"{api_url}?cmd=getTrims&make={make}&model={model}")

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Failed to fetch car details"})