from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.utils import timezone

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        vendor.calculate_on_time_delivery_rate()
        vendor.calculate_quality_rating_avg()
        vendor.calculate_average_response_time()
        vendor.calculate_fulfillment_rate()
        serializer = self.get_serializer(vendor)
        return Response(serializer.data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        purchase_order.vendor.calculate_average_response_time()
        return Response(status=status.HTTP_200_OK)