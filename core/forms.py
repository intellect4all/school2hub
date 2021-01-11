from django.forms import ModelForm
from .models import *
from django import forms

class DataForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['created', 'amount', 'ref', 'status']

class ExportForm(ModelForm):
    class Meta:
        model = Export
        exclude = ['date',]
