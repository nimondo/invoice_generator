from django import forms

from .models import Client, Product, InvoiceItem, Invoice, Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'reference', 'category', 'description', 'price', 'tva']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity']
    def __init__(self, *args, **kwargs):
        super(InvoiceItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

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
        fields = ['sex','first_name', 'last_name', 'address', 'postal_code', 'city', 'email', 'phone']
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
