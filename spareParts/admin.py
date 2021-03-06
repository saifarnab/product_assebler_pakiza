from django.contrib import admin
from .models import SparePart, Unit, Purchase, Product, EmailSettings, ProductEmailSettings
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
        'purchase_id', 'challan_no', 'supplier',  'parts_id', 'quantity', 'box', 'created_at', 'updated_at'
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'product_no', 'product_id', 'product_name', 'status', 'product_date', 'product_quantity', 'product_invoice', 'product_store', 'product_comment',
        'product_barcode', 'parts_id', 'parts_name', 'parts_unit', 'parts_box', 'parts_quantity', 'parts_invoice', 'parts_date'
    ]


class EmailAdmin(admin.ModelAdmin):
    list_display = [
        'email_id', 'email_name', 'created_at', 'updated_at'
    ]


class ProductEmailAdmin(admin.ModelAdmin):
    list_display = [
        'email_id', 'email_name', 'created_at', 'updated_at'
    ]


admin.site.register(SparePart, SparePartAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(EmailSettings, EmailAdmin)
admin.site.register(ProductEmailSettings, ProductEmailAdmin)