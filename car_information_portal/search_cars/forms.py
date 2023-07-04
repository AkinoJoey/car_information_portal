from django import forms
import requests
from datetime import date
import json

def create_year():
    current_year = date.today().year
    year_range = range(1886,current_year+1)
    year_choice = [(year,year)for year in year_range]
    return year_choice

def get_car_makes():
    headers = {'User-Agent': 'Chrome/114.0'}
    response = requests.get('https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getMakes&sold_in_us=*',headers=headers)
    # うまくjson化できないので、文字列にしてから抽出する
    res_str = response.text
    start_index = res_str.find('{')
    end_index = res_str.rfind('}')
    json_data = json.loads(res_str[start_index:end_index+1])
    makes = json_data['Makes']
    choices = []
    for make in makes:
        if make['make_country'] == 'Germany':
            choices.append((make['make_id'],make['make_display']))
    return choices

def create_car_models(makeId):
    headers = {'User-Agent': 'Chrome/114.0'}
    url = f'https://www.carqueryapi.com/api/0.3/?cmd=getModels&make={makeId}'
    response = requests.get(url=url,headers=headers)
    models = response.json()['Models']
    return models

class CarForm(forms.Form):
    make = forms.ChoiceField(choices=get_car_makes(),initial=get_car_makes()[0][0],widget=forms.Select(attrs={"id": "make","class": "mt-2 mt-sm-0 mx-sm-1 text-center"}))
    current_year = date.today().year
    begin_year = forms.ChoiceField(choices=create_year(),initial=current_year,widget=forms.Select(attrs={"class": "mt-2 mt-sm-0 mx-sm-1 text-center"}))
    end_year = forms.ChoiceField(choices=create_year(),initial=current_year,widget=forms.Select(attrs={"class": "mt-2 mt-sm-0 mx-sm-1 text-center"}))
