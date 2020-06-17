from django.contrib import admin
from .models import SparePart, Unit, Purchase
# Register your models here.


class SparePartAdmin(admin.ModelAdmin):
    list_display = [
        'parts_id', 'name', 'unit', 'quantity',  'description', 'created_at', 'updated_at'
    ]


class UnitAdmin(admin.ModelAdmin):
    list_display = [
        'unit_id', 'unit_name', 'created_at', 'updated_at'
    ]


class PurchaseAdmin(admin.ModelAdmin):
    list_display = [
        'purchase_id', 'challan_no', 'challan_date', 'supplier',  'parts_id', 'quantity', 'created_at', 'updated_at'
    ]
# class ProductAdmin(admin.ModelAdmin):
#     list_display = [
#         'product_id', 'ram', 'hdd', 'ssd', 'screen', 'created_at', 'updated_at'
#     ]


admin.site.register(SparePart, SparePartAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Purchase, PurchaseAdmin)
