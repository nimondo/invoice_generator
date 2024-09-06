from django.urls import path
from . import views

urlpatterns = [
    path('create_client/', views.create_client, name='create_client'),
    path('generate_invoice_form/<int:client_id>/', views.invoice_form, name='invoice_form'), 
    path('generate_invoice/<int:client_id>/', views.generate_invoice, name='generate_invoice'),
]