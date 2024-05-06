from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)

urlpatterns = router.urls