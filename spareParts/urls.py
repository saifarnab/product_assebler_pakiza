from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('authentication/', views.authentication, name='authentication'),
    path('sparepart/', views.add_spare_part, name='sparepart'),
    path('logout/', views.logout_session, name='logout'),
    path('producttable', views.product_tabel, name='producttable'),
    path('unittable', views.unit_table, name='unittable'),
    path('addunit', views.add_unit, name='addunit'),
    path('spareparts', views.spare_parts_table, name='spareparts'),
    path('addspareparts', views.add_spare_part, name='addspareparts'),
    path('purchases', views.purchase, name='purchases'),
    path('purchasesparts', views.purchase_parts, name='purchasesparts'),
    path(r'^unitstock/$', views.get_unit_stock, name='unitstock'),
    path(r'^changeproductstatus/$', views.change_product_status, name='changeproductstatus'),
    path('product/', views.product, name='product'),
    path('createproduct/', views.create_product, name='createproduct'),
    path('markread', views.mark_notification_read, name='markread'),
    path('notifications', views.all_notification, name='notifications'),
    path('email', views.email_settings, name='email'),
    path('addemail', views.add_email, name='addemail'),
    path(r'^deleteemail/<int:id>/', views.delete_email, name='deleteemail'),
    path(r'^emaillist/$', views.get_email_list, name='emaillist'),
    path(r'^emailsent/$', views.email_sent, name='emailsent'),
    path('productemail', views.product_email_settings, name='productemail'),
    path('productaddemail', views.product_add_email, name='productaddemail'),
    path(r'^deleteproductemail/<int:id>/', views.product_delete_email, name='deleteproductemail'),
]

