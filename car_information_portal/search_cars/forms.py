from django import forms
import requests
from datetime import date

# def create_year():
#     current_year = date.today().year
#     year_range = range(1886,current_year+1)
#     year_choice = [(year,year)for year in year_range]
#     return year_choice

# def get_car_makes():
#     headers = {'User-Agent': 'Chrome/114.0'}
#     response = requests.get('https://www.carqueryapi.com/api/0.3/?&cmd=getMakes',headers=headers)
#     makes = response.json()['Makes']
#     choices = [(make['make_id'], make['make_display']) for make in makes]
#     return choices

# class CarForm(forms.Form):
#     make = forms.ChoiceField(choices=get_car_makes())
#     model = forms.ChoiceField()
    
#     current_year = date.today().year
#     begin_year = forms.ChoiceField(choices=create_year(),initial=current_year)
#     end_year = forms.ChoiceField(choices=create_year(),initial=current_year)

# class CarForm(forms.Form):
#     make = forms.ChoiceField(choices=[], label='Make')
#     model = forms.ChoiceField(choices=[], label='Model')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['make'].choices = self.get_make_choices()
#         self.fields['make'].widget.attrs['id'] = "make_id"

#     def get_make_choices(self):
#         url = 'https://www.carqueryapi.com/api/0.3/?cmd=getMakes'
#         headers = {'User-Agent': 'Chrome/114.0'}
#         response = requests.get(url,headers=headers)
#         data = response.json()
#         choices = [(make['make_id'], make['make_display']) for make in data['Makes']]
#         return choices

def get_car_makers():
    url = 'https://www.carqueryapi.com/api/0.3/?cmd=getMakes'
    headers = {"User-Agent": "Chrome/114.0"}
    response = requests.get(url,headers=headers)
    data = response.json()
    return data['Makes']

def get_car_models(make_id):
    url = f'https://www.carqueryapi.com/api/0.3/?cmd=getModels&make={make_id}'
    headers = {"User-Agent": "Chrome/114.0"}
    response = requests.get(url,headers=headers)
    data = response.json()
    return data['Models']

class CarForm(forms.Form):
    maker_choices = []
    model_choices = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['maker'].choices = self.get_maker_choices()

    maker = forms.ChoiceField(choices=maker_choices, required=False)
    model = forms.ChoiceField(choices=model_choices, required=False)

    def get_maker_choices(self):
        makers = get_car_makers()
        choices = [('', 'Select Maker')]
        choices += [(maker['make_id'], maker['make_display']) for maker in makers]
        return choices

    def get_model_choices(self, make_id):
        models = get_car_models(make_id)
        choices = [('', 'Select Model')]
        choices += [(model['model_name'], model['model_name']) for model in models]
        return choices