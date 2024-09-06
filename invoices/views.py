from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from .models import Client, Product, Invoice, InvoiceItem
from .forms import ClientForm, InvoiceItemFormSet, ProductForm, CategoryForm


def home(request):
    return render(request, 'invoices/home.html')

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return redirect('invoice_form', client_id=client.id)  # Redirect to the invoice form with the new client ID
    else:
        form = ClientForm()

    return render(request, 'invoices/create_client.html', {'form': form})

# def invoice_form(request, client_id):
#     print("client_id:", client_id) 
#     clients = Client.objects.all()
#     selected_client = Client.objects.get(id=client_id)
#     products = Product.objects.all()
#     return render(request, 'invoices/generate_invoice.html', {
#         'clients': clients,
#         'selected_client': selected_client,
#         'products': products
#     })

def invoice_form(request, client_id):
    selected_client = Client.objects.get(id=client_id)
    products = Product.objects.all()
    
    # Initialize the forms and formset
    product_form = ProductForm()
    category_form = CategoryForm()
    formset = InvoiceItemFormSet()

    if request.method == 'POST':
        if 'add_category' in request.POST:  # If the add category form is submitted
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                category_form = CategoryForm()  # Reset the form after saving

        elif 'add_product' in request.POST:  # If the add product form is submitted
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                product_form = ProductForm()  # Reset the form after saving

        else:  # Handle the formset submission for invoice items
            formset = InvoiceItemFormSet(request.POST)
            if formset.is_valid():
                invoice = Invoice.objects.create(client=selected_client)
                for form in formset:
                    invoice_item = form.save(commit=False)
                    # Set the price based on the selected product
                    invoice_item.price = invoice_item.product.price
                    invoice_item.invoice = invoice
                    invoice_item.save()
                return redirect('generate_invoice', client_id=selected_client.id)

    return render(request, 'invoices/invoice_form.html', {
        'selected_client': selected_client,
        'formset': formset,
        'product_form': product_form,
        'category_form': category_form,
        'products': products,
    })
def generate_invoice_bk(request, client_id):
    client = Client.objects.get(id=client_id)
    products = Product.objects.all()  # Fetch all products; this would be filtered based on user selection in practice

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{client.last_name}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)

    # Draw things on the PDF. Here's where you can add text, images, etc.
    p.drawString(100, 750, f"Invoice for {client.first_name} {client.last_name}")
    p.drawString(100, 735, f"Address: {client.address}, {client.city}, {client.postal_code}")
    p.drawString(100, 720, f"Phone: {client.phone} Email: {client.email}")

    # List the products
    y = 700
    total = 0
    for product in products:
        p.drawString(100, y, f"{product.name} - {product.price}€ (TVA: {product.tva}%)")
        y -= 15
        total += product.price

    p.drawString(100, y-15, f"Total: {total}€")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response


def generate_invoice(request, client_id):
    client = Client.objects.get(id=client_id)
    invoice = Invoice.objects.filter(client=client).last()  # Get the latest invoice for this client
    items = InvoiceItem.objects.filter(invoice=invoice)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{client.last_name}.pdf"'

    # Create the PDF object, using the response object as its "file."
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Header Section
    header = Paragraph(f"<strong>Invoice for {client.first_name} {client.last_name}</strong>", styles['Title'])
    elements.append(header)

    # Client Information Section
    client_info = f"""
    <strong>Client Information</strong><br/>
    {client.first_name} {client.last_name}<br/>
    {client.address}, {client.city}, {client.postal_code}<br/>
    Phone: {client.phone}<br/>
    Email: {client.email}<br/>
    """
    elements.append(Paragraph(client_info, styles['Normal']))

    # Add spacing
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Products Table
    table_data = [["Product", "Brand", "Reference", "Category", "Price (€)", "Quantity", "Total (€)"]]
    
    for item in items:
        row = [
            item.product.name,
            item.product.brand,
            item.product.reference,
            item.product.category.name,
            f"{item.price:.2f}",
            item.quantity,
            f"{item.get_total():.2f}"
        ]
        table_data.append(row)

    # Add the total row
    total = sum(item.get_total() for item in items)
    table_data.append(["", "", "", "", "", "Total", f"{total:.2f}"])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)

    # Footer Section
    footer = Paragraph(f"Thank you for your business!", styles['Normal'])
    elements.append(footer)

    # Build the PDF
    doc.build(elements)
    return response
