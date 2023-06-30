from django import forms
import requests
from datetime import date

def create_year():
    current_year = date.today().year
    year_range = range(1886,current_year+1)
    year_choice = [(year,year)for year in year_range]
    return year_choice

def get_car_makes():
    headers = {'User-Agent': 'Chrome/114.0'}
    response = requests.get('https://www.carqueryapi.com/api/0.3/?&cmd=getMakes',headers=headers)
    makes = response.json()['Makes']
    choices = [(make['make_id'], make['make_display']) for make in makes]
    return choices

def create_car_models(makeId):
    headers = {'User-Agent': 'Chrome/114.0'}
    url = f'https://www.carqueryapi.com/api/0.3/?cmd=getModels&make={makeId}'
    response = requests.get(url=url,headers=headers)
    models = response.json()['Models']
    return models

class CarForm(forms.Form):
    make = forms.ChoiceField(choices=get_car_makes(),widget=forms.Select(attrs={"id": "make"}))
    current_year = date.today().year
    begin_year = forms.ChoiceField(choices=create_year(),initial=current_year)
    end_year = forms.ChoiceField(choices=create_year(),initial=current_year)
