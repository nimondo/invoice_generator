from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Client, Product

def generate_invoice(request, client_id):
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

def invoice_form(request):
    clients = Client.objects.all()
    products = Product.objects.all()
    return render(request, 'invoices/generate_invoice.html', {'clients': clients, 'products': products})