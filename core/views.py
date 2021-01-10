from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import DataForm, ExportForm
from django.contrib import messages
from .models import Student
from django.views import View
import requests, json
from django.conf import settings
from datetime import datetime

def Home(request):
    form = DataForm()

    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid:
            form.save()
            number = form.cleaned_data.get('phone') 
            matric = form.cleaned_data.get('matric') 
            student = Student.objects.filter(phone=number, matric=matric, status=False)[0]
            ref = student.ref
            msg = 'You order is being processed'
            messages.info(request, msg)
            return redirect('payment', ref=ref)

    context = {
        'form' : form
    }
    return render(request, 'homee.html', context)

def payment(request, ref):
    student = Student.objects.get(ref=ref)
    context = {
        'student' : student,
    }
    return render(request, 'payment.html', context)

class FlutterWaveVerification(View):
    def get(self, *args, **kwargs):
        tx_ref = self.request.GET.get('tx_ref', '')
        transaction_id = self.request.GET.get('transaction_id', '')
        status = self.request.GET.get('status', '')
        student = Student.objects.get(ref=tx_ref)

        if status == 'successful':
            url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {settings.FLUTTER_SECRET_KEY}',
            }
            res = requests.get(url, headers=headers)
            print(res)
            
            response = res.json()
            if response['status'] == 'success' and response['data']['tx_ref'] == student.ref:
                student.status = True
                student.save()
                msg = f"Dear {student.name}, You payment has been verified and the data will be credited to your sim soon. Thank you!"
                messages.info(self.request, msg)
                return redirect('home')
            else:
                student = Student.objects.get(ref=tx_ref)
                ref = student.ref
                msg = f"Dear {student.name}, Your order with reference: {tx_ref} is not yet verified. Try making the payment again. Please save this Transaction id: {transaction_id} for record process."
                messages.info(self.request, msg)
                return redirect('payment', ref =ref)
        else:
            student = Student.objects.get(ref=tx_ref)
            ref = student.ref
            msg = f"Dear {student.name}, Your payment with reference: {tx_ref} is was not successful.. Try making the payment again. Please save this Transaction id: {transaction_id} for record process."
            messages.info(self.request, msg)
            return redirect('payment', ref=ref)

def export_page (request):
    form = ExportForm()

    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data.get('month')
            day = form.cleaned_data.get('day')
            start_date=datetime(month=month, day=day, year=2021)
            end_date=datetime.now()
            students = Student.objects.filter(created__range=[start_date,end_date])
            context = {
                'students' : students
            }
            return render(request, 'result.html', context)
    context = {
        'form':form
    }
    return render (request, 'export.html', context)