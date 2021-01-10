from django.contrib import admin
from .models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    '''Admin View for Student'''

    list_display = ('matric', 'email', 'name', 'phone', 'total_gb', 'created', 'amount', 'status')
    list_filter = ('level', 'created', 'total_gb', 'status')
    readonly_fields = ('amount','ref')
    search_fields = ('name', 'email', 'phone', 'ref')
    
    