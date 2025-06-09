from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect
from patient.forms import HCPForm, PatientForm
from patient.models import Patient, ProfessionChoices, HCP
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from config.utils.decorators import role_required
from .models import MedicalRecord, MedicalRecordStatusChoices, PaymentStatusChoices
from django.views.decorators.http import require_http_methods
from .forms import MedicalRecordForm
import json


@login_required
@role_required(allowed_roles=['ADMIN', 'RECEPTIONIST', 'DOCTOR'])
def home(request):

    allpatients = Patient.objects.filter(user = request.user)

    context = {
        'patients': allpatients,
        'status_choices': MedicalRecordStatusChoices.choices,
        'payment_choices': PaymentStatusChoices.choices,     
        'hcps': HCP.objects.filter(user=request.user),  
    }

    return render(request, 'patient/home.html', context)


def patient_register(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()

            # Check if request is AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)

    # If it's GET or non-AJAX fallback
    form = PatientForm()
    return render(request, 'patient/patient_register.html', {'form': form})

def patient_edit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('home')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)

    # Optional: render form if needed for GET
    form = PatientForm(instance=patient)
    return render(request, 'patient/patient_register.html', {'form': form})


def patient_delete(request, patient_id):
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(id=patient_id)
            patient.delete()
            return JsonResponse({'success': True})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def send_email_to_patient(request, patient_id):
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(id=patient_id)
            recipient = patient.email if hasattr(patient, 'email') else None  # Make sure email field exists

            if not recipient:
                return JsonResponse({'success': False, 'error': 'Email address not found.'})

            send_mail(
                subject='Important Message from Clinic',
                message=f'Dear {patient.fullname},\n\nThis is a test email from the system.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def hcp_manage(request):

    allHcp = HCP.objects.filter(user = request.user)

    context = {
        'allhcps': allHcp,
         'professions': ProfessionChoices.choices,  # For dropdown
    }

    return render(request, 'patient/hcp_list.html', context)


def hcp_register(request):
    if request.method == 'POST':
        form = HCPForm(request.POST)
        if form.is_valid():
            hcp = form.save(commit=False)
            hcp.user = request.user
            hcp.save()

            # Check if request is AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('hcp_manage')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)

    # If it's GET or non-AJAX fallback
    form = HCPForm()
    return render(request, 'patient/hcp_list.html', {'form': form})
    

def hcp_edit(request, hcp_id):
    hcp = get_object_or_404(HCP, id=hcp_id)

    if request.method == 'POST':
        form = HCPForm(request.POST, instance=hcp)
        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('hcp_register')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)

    # Optional: render form if needed for GET
    form = PatientForm(instance=hcp)
    return render(request, 'patient/patient_register.html', {'form': form})


def get_medical_records(request, patient_id):
    try:
        records = MedicalRecord.objects.filter(patient_id=patient_id).select_related('hcp')
        
        if hasattr(request.user, 'hcp'):
            records = records.filter(hcp__user=request.user)
        
        data = [{
            'id': record.id,
            'date': record.date.strftime('%Y-%m-%d'),
            'hcp': record.hcp.fullname,
            'hcp_id': record.hcp.id,  # Add this line
            'status': record.status,
            'payment_status': record.payment_status,
        } for record in records]
        
        return JsonResponse({'success': True, 'records': data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def add_medical_record(request):
    try:
        data = json.loads(request.body)
        form = MedicalRecordForm(data, user=request.user)
        
        if form.is_valid():
            record = form.save(commit=False)
            record.patient_id = data.get('patient_id')
            record.save()
            return JsonResponse({'success': True, 'record': {
                'id': record.id,
                'date': record.date.strftime('%Y-%m-%d'),
                'hcp': record.hcp.fullname,
                'status': record.status,
                'payment_status': record.payment_status,
            }})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    

def edit_medical_record(request, record_id):
    try:
        record = MedicalRecord.objects.get(id=record_id)
        # Security: HCPs can only edit their own records
        if hasattr(request.user, 'hcp') and record.hcp.user != request.user:
            return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
        
        data = json.loads(request.body)
        form = MedicalRecordForm(data, instance=record, user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()}, status=400)
    except MedicalRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)
    

def delete_medical_record(request, record_id):
    try:
        record = MedicalRecord.objects.get(id=record_id)
        # Security: HCPs can only delete their own records
        if hasattr(request.user, 'hcp') and record.hcp.user != request.user:
            return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
        
        record.delete()
        return JsonResponse({'success': True})
    except MedicalRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)
    
