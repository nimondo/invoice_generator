Here's a README file template for your Django invoice management project:

---

# Invoice Management System

This project is a Django-based web application for managing invoices. It allows users to create, update, and manage clients and products, generate invoices, and download them as PDF files.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Models](#models)
  - [Client](#client)
  - [Product](#product)
  - [Category](#category)
  - [Invoice](#invoice)
  - [InvoiceItem](#invoiceitem)
- [Forms](#forms)
- [Views](#views)
- [PDF Generation](#pdf-generation)
- [License](#license)

## Features

- Client management (add, edit, delete)
- Product management with category support
- Dynamic formsets for adding multiple products to an invoice
- Invoice generation with client and product details
- Download invoices as PDF files
- User-friendly forms with Bootstrap styling

## Installation

### Prerequisites

- Python 3.x
- Django 3.x or later
- ReportLab for PDF generation

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/invoice-management-system.git
   cd invoice-management-system
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

6. **Access the application:**

   Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

1. **Create a client:**
   - Navigate to the "Create Client" page.
   - Fill in the client's details, including the new "Sex" field.

2. **Create a product:**
   - Navigate to the "Create Product" page.
   - Select or create a category and fill in the product details.

3. **Generate an invoice:**
   - Go to the "Generate Invoice" page.
   - Select the client and add multiple products.
   - Generate the invoice and download it as a PDF.

## Project Structure

```bash
invoice_management_system/
│
├── invoices/
│   ├── migrations/
│   ├── templates/
│   │   └── invoices/
│   │       ├── base.html
│   │       ├── invoice_form.html
│   │       ├── generate_invoice.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│
├── invoice_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── manage.py
└── README.md
```

## Models

### Client

The `Client` model includes the following fields:

- `first_name`: The client's first name.
- `last_name`: The client's last name.
- `address`: The client's address.
- `postal_code`: The client's postal code.
- `city`: The client's city.
- `email`: The client's email address.
- `phone`: The client's phone number.
- `sex`: The client's sex (`M` for Male, `F` for Female).

### Product

The `Product` model includes:

- `name`: The product's name.
- `brand`: The product's brand.
- `reference`: The product's reference number.
- `category`: The category the product belongs to.
- `description`: A description of the product.
- `price`: The price of the product.
- `tva`: The VAT applied to the product.

### Category

The `Category` model includes:

- `name`: The name of the category.

### Invoice

The `Invoice` model includes:

- `client`: The client associated with the invoice.
- `invoice_number`: A unique identifier for the invoice.
- `created_at`: The date and time the invoice was created.

### InvoiceItem

The `InvoiceItem` model includes:

- `invoice`: The associated invoice.
- `product`: The product added to the invoice.
- `quantity`: The quantity of the product.
- `price`: The price of the product at the time of the invoice.

## Forms

- **ClientForm**: Manages client data.
- **ProductForm**: Manages product data.
- **CategoryForm**: Manages category data.
- **InvoiceItemFormSet**: Handles multiple product entries for an invoice.

## Views

- **invoice_form**: Handles creating and managing invoices, including adding products and categories.
- **generate_invoice**: Generates a PDF invoice with all client and product details.

## PDF Generation

The invoice PDF includes:

- Client information
- Invoice number
- List of products with their details and total price
- Generated using the ReportLab library

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
