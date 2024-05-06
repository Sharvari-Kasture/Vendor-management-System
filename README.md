# Vendor-management-System

This project is a Vendor Management System developed using Django and Django REST Framework. The system allows users to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Setup Instructions

### Prerequisites
- Python (3.6+)
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vendor-management-system.git
   cd vendor-management-system

2.Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate  # For Linux/macOS
         venv\Scripts\activate.bat # For Windows 

3.Install dependencies:
  pip install django
  pip install djangorestframework

4.Apply database migrations:
  python manage.py makemigrations
  python manage.py migrate
  Running the Development Server
  Start the Django development server:
  python manage.py runserver
  The server will start at http://127.0.0.1:8000/.

API Endpoints

Vendors

GET /api/vendors/: List all vendors.

POST /api/vendors/: Create a new vendor.

GET /api/vendors/{vendor_id}/: Retrieve details of a specific vendor.

PUT /api/vendors/{vendor_id}/: Update a vendor's details.

DELETE /api/vendors/{vendor_id}/: Delete a vendor.

GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance metrics.


Purchase Orders

GET /api/purchase_orders/: List all purchase orders.

POST /api/purchase_orders/: Create a new purchase order.

GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.

PUT /api/purchase_orders/{po_id}/: Update a purchase order.

DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

POST /api/purchase_orders/{po_id}/acknowledge: Acknowledge a purchase order.

