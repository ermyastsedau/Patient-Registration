from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patients/edit/<int:patient_id>/', views.patient_edit, name='patient_edit'),
    path('patients/delete/<int:patient_id>/', views.patient_delete, name='patient_delete'),
    path('patients/send-email/<int:patient_id>/', views.send_email_to_patient, name='send_email_to_patient'),
    path('hcp_manage/', views.hcp_manage, name='hcp_manage'),
    path('hcp_manage/register', views.hcp_register, name='hcp_register'),
    path('hcp_manage/edit/<int:hcp_id>/', views.hcp_edit, name='hcp_edit'),
    path('patients/<int:patient_id>/medical-records/', views.get_medical_records, name='get_medical_records'),
    path('patients/medical-records/add/', views.add_medical_record, name='add_medical_record'),
    path('patients/medical-records/edit/<int:record_id>/', views.edit_medical_record, name='edit_medical_record'),
    path('patients/medical-records/delete/<int:record_id>/', views.delete_medical_record, name='delete_medical_record'),
]