from django import forms

from django_user_agents.utils import get_user_agent
from .models import Food, Recipe, Plan, Inventory
from tinymce.widgets import TinyMCE
from multiselectfield import MultiSelectField
from django.conf import settings

choices = (
    ('1', 'Meat'),
    ('2', 'Veggie'),
    ('3', 'Spice')
)


class FoodForm(forms.ModelForm):
#
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'style': 'font-size:30px; -webkit-text-stroke-width: .5px;-webkit-text-stroke-color: #181d27;width: 80%;  color: #181d27; margin-left: auto; margin-right: auto; background-color:#69b578; border: 6px dotted black'}))
    ftype = forms.ChoiceField(label='Type', choices=choices, widget=forms.Select(attrs={'class':'form-control', 'style': 'font-size:30px; -webkit-text-stroke-width: .5px;-webkit-text-stroke-color: #181d27;width: 80%; height: 70px; color: #181d27; margin-left: auto; margin-right: auto; background-color:#69b578; border: 6px dotted black'}))
    cost = forms.DecimalField(label='Cost', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'style': 'font-size:30px; -webkit-text-stroke-width: .5px;-webkit-text-stroke-color: #181d27;width: 80%; color: #181d27; margin-left: auto; margin-right: auto; background-color:#69b578; border: 6px dotted black'}))
    qty = forms.IntegerField(label='QTY', widget=forms.TextInput(attrs={'style': 'font-size: 30px; -webkit-text-stroke-width: .5px; -webkit-text-stroke-color: #181d27; width: 80%; color: #181d27; margin-left: auto; margin-right: auto; background-color:#69b578; border: 6px dotted black'}))
    description = forms.CharField(label='Description', widget=forms.TextInput(attrs={'style': 'font-size:16px;width: 80%; color: #181d27; margin-left: auto; margin-right: auto; background-color:#69b578; border: 6px dotted black'}))

    class Meta:
        model = Food
        fields = ['name', 'ftype', 'cost', 'qty', 'description']

class RecipeForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'style': 'font-size: 24px; -webkit-text-stroke-width: .5px; text-align: center; -webkit-text-stroke-color: #181d27; width: 100%; color: #181d27; margin-left: auto; margin-right: auto; background-color:#69b578'}))

    food = forms.CharField(label='Ingredients', widget=forms.TextInput(attrs={'id': 'extraField', 'style': 'font-size: 24px; -webkit-text-stroke-width: .5px; text-align: center; -webkit-text-stroke-color: #181d27; width: 80%; color: #181d27; margin-left: 6%; margin-right: auto; background-color:#69b578'}))


    #cost = forms.DecimalField(label='Cost', max_digits=5, decimal_places=2, widget=forms.TextInput(attrs={'style': 'font-size: 24px; width: 50%; text-align: center; color: #181d27;border-bottom: 1px solid #181d27;'}))
    description = forms.CharField(label='Description', widget=TinyMCE(attrs={'style': 'background-color:#69b578;border: 6px dotted black; height: 400px'}))
    def __init__(self, *args, **kwargs):
        extra_list = []
        extra_fields = kwargs.pop('extra', 0)
        extra_list.append(extra_fields)
        super(RecipeForm, self).__init__(*args, **kwargs)

        for index in range(0, int(len(extra_list)) + 1):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = \
                forms.CharField()





class PlanForm(forms.Form):
    meal = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'json'}), label='jsoncalendar', required=False)
    day = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'json2'}), label='jsoncalendar', required=False)
