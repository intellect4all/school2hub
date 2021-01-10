from django.forms import ModelForm
from .models import *

class DataForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['created', 'amount', 'ref', 'status']