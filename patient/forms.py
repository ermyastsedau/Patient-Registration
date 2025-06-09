from django import forms
from .models import Patient, HCP, MedicalRecord

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['fullname', 'date_of_birth', 'gender', 'phone_number','email', 'address']


class HCPForm(forms.ModelForm):
    class Meta:
        model = HCP
        fields = ['fullname', 'phone_number', 'email', 'profession']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['date', 'hcp', 'status', 'payment_status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'hcp'):
            self.fields['hcp'].queryset = HCP.objects.filter(user=user)
            self.fields['hcp'].initial = user.hcp

