from datetime import datetime

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import SparePart, Unit, Purchase, Product
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Max


def login(request):
    return render(request, 'authentication-login.html', {})


def authentication(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = authenticate(username=email, password=password)
    if user is None:
        return render(request, 'authentication-login.html', {'message': 'Invalid Username or Password!'})
    request.session['user'] = email
    return redirect(unit_table)


def logout_session(request):
    logout(request)
    return redirect('login')


def unit_table(request):
    if 'user' not in request.session:
        return redirect('login')
    unit = Unit.objects.all()
    linked_content = []
    for content in unit:
        linked_content.append(content.__dict__)
    print(linked_content)
    return render(request, 'tables.html', {'data': linked_content, 'user': request.session['user']})


def add_unit(request):
    if 'user' not in request.session:
        return redirect('login')
    if request.POST:
        unit = request.POST.get('unit', '')
        if unit != '':
            if Unit.objects.filter(unit_name=unit).exists():
                return render(request, 'add_unit.html', {'user': request.session['user'], 'message': f"'{unit}' already exists"})
            Unit.objects.create(unit_name=unit)
            return redirect(unit_table)
    return render(request, 'add_unit.html', {'user': request.session['user']})


def spare_parts_table(request):
    if 'user' not in request.session:
        return redirect('login')
    parts = SparePart.objects.all()
    linked_content = []
    for content in parts:
        linked_content.append(content.__dict__)
    print(linked_content)
    return render(request, 'spare_parts_tables.html', {'data': linked_content, 'user': request.session['user']})


def add_spare_part(request):
    if 'user' not in request.session:
        return redirect('login')

    linked_content = []
    unit = Unit.objects.all()
    for content in unit:
        linked_content.append(content.__dict__)
    print(linked_content)
    if request.method == "POST":
        name = request.POST.get('name', '')
        unit = request.POST.get('unit', '')
        description = request.POST.get('description', '')
        if SparePart.objects.filter(name=name, unit=unit).exists():
            message = 'Spare Part already exists'
            return render(request, 'add_spare_parts.html',
                          {'data': linked_content, 'user': request.session['user'], 'message': message})
        if name != '' and unit != '-1':
            SparePart.objects.create(name=name, unit=unit, description=description)
            return redirect(spare_parts_table)
        else:
            message = 'Name and Unit can not empty'
            return render(request, 'add_spare_parts.html', {'data': linked_content, 'user': request.session['user'], 'message': message})
    return render(request, 'add_spare_parts.html', {'data': linked_content, 'user': request.session['user']})


def purchase(request):
    if 'user' not in request.session:
        return redirect('login')
    purchase = Purchase.objects.all()
    linked_content = []
    for content in purchase:
        linked_content.append(content.__dict__)
    return render(request, 'purchase.html', {'data': linked_content, 'user': request.session['user']})


def purchase_parts(request):
    if 'user' not in request.session:
        return redirect('login')
    linked_content = []
    parts = SparePart.objects.all()
    for content in parts:
        linked_content.append(content.__dict__)

    if request.method == "POST":
        try:
            val = int(request.POST.get('total', ''))
            print('val', val)
            count = 1
            check = 0
            while (1):
                supplier = request.POST.get('supplier_' + str(count), '')
                challan = request.POST.get('challan_' + str(count), '')
                parts_id = request.POST.get('partsid_' + str(count), '')
                quantity = request.POST.get('quantity_' + str(count), '')
                box = request.POST.get('box_' + str(count), '')
                print('box', box)
                date = request.POST.get('date_' + str(count), '')
                date = datetime.strptime(date[2:], '%y-%m-%d').date()
                if supplier != '' and challan != '' and parts_id != '' and quantity != '':
                    parts_id = int(parts_id)
                    quantity = int(quantity)
                    qry = SparePart.objects.filter(parts_id=parts_id).values_list('quantity')
                    qry_list = list(qry)
                    current_quantity = qry_list[0][0]
                    if current_quantity is None:
                        current_quantity = 0
                    total_quantity = current_quantity + quantity
                    SparePart.objects.filter(parts_id=parts_id).update(quantity=total_quantity)
                    try:
                        print(supplier, challan, parts_id, quantity)
                        Purchase.objects.create(supplier=supplier, challan_no=challan, parts_id=parts_id, quantity=quantity, box=box, created_at=date)
                    except:
                        print('error creating purchase')
                    check += 1
                count += 1
                if check == val:
                    break
                if count > 50:
                    break
                break
        except:
            print('error in val')
            return redirect(purchase_parts)
        while True:
            break
        print(val)
    return render(request, 'purchase_spare_parts.html', {'data': linked_content, 'user': request.session['user']})


def get_unit_stock(request):
    data = int(request.GET['id'])
    if data < 1:
        data = 'Spare Part Unit Here' + ', ' + 'Spare Part Available Stock Here'
        return HttpResponse(data)
    qry = SparePart.objects.filter(parts_id=data).values_list('quantity', 'unit', 'name', )
    qry_list = list(qry)
    stock = str(qry_list[0][0])
    if qry_list[0][0] is None:
        stock = 0
    data = str(qry_list[0][1]) + ', ' + str(stock) + ', ' + str(qry_list[0][2])
    print(data)
    return HttpResponse(data)


def product(request):
    if 'user' not in request.session:
        return redirect('login')
    args = Product.objects.filter()
    maxProductNo = args.aggregate(Max('product_no')).get('product_no__max')
    if maxProductNo is None:
        maxProductNo = 1
    linked_content = []
    for i in range(maxProductNo):
        if Product.objects.filter(product_no=i+1).exists():
            product = list(Product.objects.filter(product_no=i+1).values_list("product_name", "product_barcode", "parts_name", "parts_quantity", "parts_unit" ))
            parts = []
            for item in range(len(product)):
                thisdict = {
                    'parts_name': product[item][2],
                    'quantity': product[item][3],
                    'unit': product[item][4]
                }
                parts.append(thisdict)
            custom_dict = {
                'product_no': i + 1,
                'product_name': product[0][0],
                'barcode': product[0][1],
                'parts_list': parts,
            }
            linked_content.append(custom_dict)

    print(linked_content)
    return render(request, 'product.html', {'data': linked_content, 'user': request.session['user']})


def create_product(request):
    if 'user' not in request.session:
        return redirect('login')
    linked_content = []
    parts = SparePart.objects.all()
    for content in parts:
        linked_content.append(content.__dict__)
    if request.method == "POST":

        try:
            val = int(request.POST.get('total', ''))
            print('hit create product')
            count = 1
            check = 0
            while (1):
                name = request.POST.get('name_' + str(count), '')
                product_id = request.POST.get('product_id_' + str(count), '')
                print('product_id', product_id)
                store = request.POST.get('store_' + str(count), '')
                product_invoice = request.POST.get('product_invoice_' + str(count), '')
                product_quantity = request.POST.get('product_quantity_' + str(count), '')
                product_quantity = int(product_quantity)
                comment = request.POST.get('comment_' + str(count), '')
                date = request.POST.get('date_' + str(count), '')
                date = datetime.strptime(date[2:], '%y-%m-%d').date()
                unit = request.POST.get('unit_' + str(count), '')
                barcode = request.POST.get('barcode_' + str(count), '')
                partsname = request.POST.get('partsname_' + str(count), '')
                parts_id = request.POST.get('partsid_' + str(count), '')
                parts_date = request.POST.get('parts_date_' + str(count), '')
                parts_invoice = request.POST.get('parts_invoice_' + str(count), '')
                parts_box = request.POST.get('box_' + str(count), '')
                parts_date = datetime.strptime(parts_date[2:], '%y-%m-%d').date()
                quantity = request.POST.get('quantity_' + str(count), '')
                print('*****', product_invoice, product_quantity)
                if partsname != '' and parts_id != '' and quantity != '':
                    parts_id = int(parts_id)
                    quantity = int(quantity)
                    qry = SparePart.objects.filter(parts_id=parts_id).values_list('quantity')
                    qry_list = list(qry)
                    current_quantity = qry_list[0][0]
                    if current_quantity is None:
                        current_quantity = 1
                    if quantity > current_quantity:
                        return render(request, 'create_product.html', {'data': linked_content, 'user': request.session['user']})
                    print(product_id, unit, name, parts_invoice, barcode, partsname, parts_id, parts_box, quantity, store, comment, date, parts_date, product_quantity, product_invoice)
                    Product.objects.create(product_id=product_id, parts_unit=unit, product_name=name, parts_invoice=parts_invoice,
                                           product_barcode=barcode, parts_name=partsname, parts_id=parts_id, parts_box=parts_box,
                                           parts_quantity=quantity, product_store=store, product_comment=comment,
                                           product_quantity=product_quantity, product_invoice=product_invoice)
                    check += 1
                count += 1
                if check == val:
                    return redirect(product)
        except:
            print('error')
            return redirect(create_product)
    return render(request, 'create_product.html', {'data': linked_content, 'user': request.session['user']})
# def add_product(request):
#     if 'user' not in request.session:
#         return redirect('login')
#
#     ram = SparePart.objects.filter(type='Ram')
#     hdd = SparePart.objects.filter(type='HDD')
#     ssd = SparePart.objects.filter(type='SSD')
#     screen = SparePart.objects.filter(type='Screen Size')
#
#     ram_list = []
#     hdd_list = []
#     ssd_list = []
#     screen_list = []
#
#     for item in ram:
#         ram_item = item.name + ' ' + item.measurement_unit_scale + ' ' + item.measurement_unit
#         ram_list.append({'key': item.parts_id, 'value': ram_item})
#     for item in hdd:
#         hdd_item = item.name + ' ' + item.measurement_unit_scale + ' ' + item.measurement_unit
#         hdd_list.append({'key': item.parts_id, 'value': hdd_item})
#     for item in ssd:
#         ssd_item = item.name + ' ' + item.measurement_unit_scale + ' ' + item.measurement_unit
#         ssd_list.append({'key': item.parts_id, 'value': ssd_item})
#     for item in screen:
#         screen_item = item.name + ' ' + item.measurement_unit_scale + ' ' + item.measurement_unit
#         screen_list.append({'key': item.parts_id, 'value': screen_item})
#
#     if request.method == "POST":
#         message = []
#         ram = request.POST.get('ram', '')
#         ram_quantity = request.POST.get('ram_quantity', '')
#         hdd = request.POST.get('hdd', '')
#         hdd_quantity = request.POST.get('ram_quantity', '')
#         ssd = request.POST.get('ssd', '')
#         ssd_quantity = request.POST.get('ssd_quantity', '')
#         screen = request.POST.get('screen', '')
#         screen_quantity = request.POST.get('screen_quantity', '')
#         print(type(ssd))
#         try:
#             if ram != '0':
#                 ram_db = SparePart.objects.get(parts_id=int(ram))
#                 if int(ram_quantity) >= int(ram_db.quantity):
#                     message.append(f'only {ram_db.quantity} piece of ram available in stock')
#
#             if hdd != '0':
#                 hdd_db = SparePart.objects.get(parts_id=int(hdd))
#                 if int(hdd_quantity) >= int(hdd_db.quantity):
#                     message.append(f'only {hdd_db.quantity} piece of hdd available in stock')
#
#             if ssd != '0':
#                 ssd_db = SparePart.objects.get(parts_id=int(ssd))
#                 if int(ssd_quantity) >= int(ssd_db.quantity):
#                     message.append(f'only {ssd_db.quantity} piece of ssd available in stock')
#
#             if screen != '0':
#                 screen_db = SparePart.objects.get(parts_id=int(screen))
#                 if int(screen_quantity) >= int(screen_db.quantity):
#                     message.append(f'only {screen_db.quantity} piece of screen available in stock')
#
#             if Product.objects.filter(ram=int(ram), hdd=int(hdd), ssd=int(ssd), screen=int(screen)).exists():
#                 message.append('Product already available')
#
#             if message:
#                 return render(request, 'add-product.html', {'ram': ram_list, 'hdd': hdd_list, 'ssd': ssd_list, 'screen': screen_list, 'message': message})
#             Product.objects.create(ram=int(ram), hdd=int(hdd), ssd=int(ssd), screen=int(screen))
#         except:
#             message.append('Invalid Input')
#             return render(request, 'add-product.html', {'ram': ram_list, 'hdd': hdd_list, 'ssd': ssd_list, 'screen': screen_list, 'message':message})
#
#     return render(request, 'add-product.html', {'ram': ram_list, 'hdd': hdd_list, 'ssd': ssd_list, 'screen': screen_list, 'user': request.session['user']})


def product_tabel(request):
    return render(request, 'tables.html', {})