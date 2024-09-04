from django.urls import path
from . import views

urlpatterns = [
    path('generate_invoice_form/', views.invoice_form, name='invoice_form'),
    path('generate_invoice/<int:client_id>/', views.generate_invoice, name='generate_invoice'),
]
