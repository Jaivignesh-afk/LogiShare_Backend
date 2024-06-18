from django.contrib import admin
from .models import Shipment, Transporter, Customer 

# Register your models here.
class CustomerListAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone_number']

class ShipmentListAdmin(admin.ModelAdmin):
    list_display = ['id', 'transporter']

admin.site.register(Shipment, ShipmentListAdmin)
admin.site.register(Transporter)
admin.site.register(Customer, CustomerListAdmin)
