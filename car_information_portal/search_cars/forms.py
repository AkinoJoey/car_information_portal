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
    url = 'https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getMakes&sold_in_us=*'
    response = requests.get(url=url,headers=headers)
    # うまくjson化できないので、文字列にしてから抽出する
    res_str = response.text
    json_data = convert_text_to_json(res_str)
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

def get_car_models_choices(makeId):
    headers = {'User-Agent': 'Chrome/114.0'}
    url = f'https://www.carqueryapi.com/api/0.3/?cmd=getModels&make={makeId}'
    response = requests.get(url=url,headers=headers)
    models = response.json()['Models']
    choices = []
    choices.append(('', '----'))
    for model in models:
        choices.append((model['model_name'],model['model_name']))
    return choices

def get_car_data(make_id,model,begin_year,end_year):
    headers = {'User-Agent': 'Chrome/114.0'}
    url = f'https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getTrims&model_make_id={make_id}&model={model}'
    response = requests.get(url=url,headers=headers)
    json_data = convert_text_to_json(response.text)
    all_data = json_data['Trims']
    res = []
    for data in all_data:
        model_year = int(data['model_year'])
        if model_year >= begin_year and model_year <= end_year:
            res.append((data['model_name'],data['model_year'],data['model_engine_power_ps'],data['model_engine_cc']))
    return res

def create_car_models_by_year(make_id,year):
    headers = {'User-Agent': 'Chrome/114.0'}
    url = f"https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getTrims&make={make_id}&year={year}"
    response = requests.get(url=url,headers=headers)
    # うまくjson化できないので、文字列にしてから抽出する
    res_str = response.text
    json_data = convert_text_to_json(res_str)
    all_data = json_data['Trims']
    dict = {}
    for data in all_data:
        model = data['model_name']
        dict.setdefault(model,model)
    return list(dict.keys())

def get_min_year():
    headers = {'User-Agent': 'Chrome/114.0'}
    url = 'https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getYears'
    response = requests.get(url=url,headers=headers)
    res_str = response.text
    json_data = convert_text_to_json(res_str)
    years = json_data['Years']
    
    return years['min_year']

def get_max_year():
    headers = {'User-Agent': 'Chrome/114.0'}
    url = 'https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getYears'
    response = requests.get(url=url,headers=headers)
    res_str = response.text
    json_data = convert_text_to_json(res_str)
    years = json_data['Years']
    
    return years['max_year']

def convert_text_to_json(text):
    start_index = text.find('{')
    end_index = text.rfind('}')
    json_data = json.loads(text[start_index:end_index+1])
    return json_data
    
class CarForm(forms.Form):   
    makes_choices = get_car_makes()
    make = forms.ChoiceField(choices=makes_choices,
                                required=True,
                                widget=forms.Select(attrs={"id": "make","class": "mt-2 mt-sm-0 mx-sm-1 text-center"}))
    
    model = forms.ChoiceField(widget=forms.Select(attrs={"id": "model","class": "mt-2 mt-sm-0 mx-sm-1 text-center"}))
    
    current_year = date.today().year
    begin_year_choices = create_year()
    
    begin_year = forms.ChoiceField(choices=begin_year_choices,
                                    widget=forms.Select(attrs={"class": "mt-2 mt-sm-0 mx-sm-1 text-center"}))
    end_year_choices = create_year()
    end_year = forms.ChoiceField(choices=end_year_choices,
                                    widget=forms.Select(attrs={"class": "mt-2 mt-sm-0 mx-sm-1 text-center"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['make'].initial = self.makes_choices[0][0]
        self.fields['model'].initial = self.set_model_choices(self.fields['make'].initial)
        self.fields['begin_year'].initial = self.current_year
        self.fields['end_year'].initial = self.current_year
    
        
    def set_model_choices(self,make_id):
        self.fields['model'].choices = get_car_models_choices(make_id)
        
    def set_model_initial(self,model):
        self.fields['model'].initial = model

    def get_make_display(self,make_id):
        for choice in self.makes_choices:
                if choice[0] == make_id:
                    return choice[1]