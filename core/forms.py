from django.forms import ModelForm
from .models import *
from django import forms

class DataForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['created', 'amount', 'ref', 'status']

class ExportForm(forms.Form):
    month = forms.IntegerField(max_value=12)
    day = forms.IntegerField(max_value=31, required=False)