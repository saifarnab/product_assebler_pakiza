from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('authentication/', views.authentication, name='authentication'),
    path('sparepart/', views.add_spare_part, name='sparepart'),
    # path('addproduct/', views.add_product, name='addproduct'),
    path('logout/', views.logout_session, name='logout'),
    path('producttable', views.product_tabel, name='producttable'),
    path('unittable', views.unit_table, name='unittable'),
    path('addunit', views.add_unit, name='addunit'),
    path('spareparts', views.spare_parts_table, name='spareparts'),
    path('addspareparts', views.add_spare_part, name='addspareparts'),
    path('purchases', views.purchase, name='purchases'),
    path('purchasesparts', views.purchase_parts, name='purchasesparts'),
    path(r'^unitstock/$', views.get_unit_stock, name='unitstock'),
    path('product/', views.product, name='product'),
    path('createproduct/', views.create_product, name='createproduct'),
]

