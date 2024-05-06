
from django.db import models
from django.db.models import Avg, Count, F
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def _str_(self):
        return self.name

    def calculate_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            on_time_orders = completed_orders.filter(delivery_date__lte=F('acknowledgment_date'))
            on_time_delivery_rate = (on_time_orders.count() / total_completed_orders) * 100
            self.on_time_delivery_rate = round(on_time_delivery_rate, 2)
            self.save()

    def calculate_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(status='completed').exclude(quality_rating=None)
        if completed_orders.exists():
            quality_rating_avg = completed_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']
            self.quality_rating_avg = round(quality_rating_avg, 2)
            self.save()

    def calculate_average_response_time(self):
        acknowledged_orders = self.purchaseorder_set.filter(status='acknowledged')
        if acknowledged_orders.exists():
            response_times = []
            for order in acknowledged_orders:
                response_time = order.acknowledgment_date - order.issue_date
                response_times.append(response_time.total_seconds())
            if response_times:
                average_response_time = sum(response_times) / len(response_times)
                self.average_response_time = round(average_response_time / 3600, 2)  # Convert to hours
                self.save()

    def calculate_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        if total_orders > 0:
            successful_orders = self.purchaseorder_set.filter(status='completed')
            fulfillment_rate = (successful_orders.count() / total_orders) * 100
            self.fulfillment_rate = round(fulfillment_rate, 2)
            self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def _str_(self):
        return self.po_number

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, created, **kwargs):
    if instance.vendor:
        instance.vendor.calculate_on_time_delivery_rate()
        instance.vendor.calculate_quality_rating_avg()
        instance.vendor.calculate_fulfillment_rate()

    if instance.status == 'acknowledged':
        instance.vendor.calculate_average_response_time()