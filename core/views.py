from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import DataForm, ExportForm
from django.contrib import messages
from .models import Student
from django.views import View
import requests, json
from django.conf import settings
from datetime import datetime
from django.utils import timezone
import csv

def Home(request):
    form = DataForm()

    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
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
        print("form entry point")
        if form.is_valid():
            month = form.cleaned_data.get('month')
            day = form.cleaned_data.get('day')
            if month != '' and day != '':
                start_date_naive=datetime(month=month, day=day, year=2021)
                print(f'{start_date_naive} entry')
                current_tz = timezone.get_current_timezone()
                start_date = current_tz.localize(start_date_naive)
                end_date=timezone.now()
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="completed_reg_exports.csv"'
                writer = csv.writer(response)
                writer.writerow(['id', 'matric', 'email', 'name', 'phone', 'total_gb', 'created', 'amount'])
                data = Student.objects.filter(created__range=[start_date,end_date], status=True).values_list('id', 'matric', 'email', 'name', 'phone', 'total_gb', 'created', 'amount')
                print('database connection stage')
                for entry in data:
                    writer.writerow(entry)
                    print('data entry stage')
                return response
            else :
                msg = f"Error Exporting, please select date and try again"
                print('error with month and date.')
                messages.info(request, msg)
                return redirect('export')
        else :
                msg = f"Form is not valid"
                print('Error with form validity')
                messages.info(request, msg)
                return redirect('export')

    context = {
        'form':form
    }
    return render (request, 'export.html', context)