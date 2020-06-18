from django.db import models


class Unit(models.Model):
    unit_id = models.BigAutoField(primary_key=True)
    unit_name = models.CharField(max_length=288, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SparePart(models.Model):
    parts_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=288, blank=False, null=False)
    unit = models.CharField(max_length=288, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    quantity = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Purchase(models.Model):
    purchase_id = models.BigAutoField(primary_key=True)
    challan_no = models.CharField(max_length=288, blank=False, null=False)
    supplier = models.CharField(max_length=288, blank=False, null=False)
    parts_id = models.BigIntegerField(null=False, blank=False)
    quantity = models.BigIntegerField(null=True, blank=True)
    box = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_no = models.BigIntegerField(null=False, blank=False)
    product_name = models.CharField(max_length=288, blank=False, null=False)
    parts_id = models.BigIntegerField(null=False, blank=False)
    parts_name = models.CharField(max_length=288, blank=False, null=False)
    parts_unit = models.CharField(max_length=288, blank=False, null=False)
    quantity = models.IntegerField(null=False, blank=False)
    barcode = models.CharField(max_length=288, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




# class Product(models.Model):
#     product_id = models.BigAutoField(primary_key=True)
#     ram = models.BigIntegerField(null=True, blank=True)
#     hdd = models.BigIntegerField(null=True, blank=True)
#     ssd = models.BigIntegerField(null=True, blank=True)
#     screen = models.BigIntegerField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
