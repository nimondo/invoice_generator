from django import forms

from .models import Client, Product, InvoiceItem, Invoice, Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'reference', 'category', 'description', 'price', 'tva']
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity']

# Create a formset to manage multiple InvoiceItem forms
InvoiceItemFormSet = forms.inlineformset_factory(
    parent_model=Invoice, 
    model=InvoiceItem, 
    form=InvoiceItemForm, 
    extra=1, 
    can_delete=True
)
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'address', 'postal_code', 'city', 'email', 'phone']
