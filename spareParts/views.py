import base64
from datetime import datetime
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import SparePart, Unit, Purchase, Product, EmailSettings
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Max
from notifications.signals import notify
from django.http import HttpResponseRedirect
import barcode
from barcode.writer import ImageWriter
from django.core.mail import send_mail
from django.conf import settings


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
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    unit = Unit.objects.all()
    linked_content = []
    for content in unit:
        linked_content.append(content.__dict__)
    print(notification_list)
    return render(request, 'tables.html', {'notification': notification_list, 'data': linked_content, 'user': request.session['user']})


def add_unit(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    if request.POST:
        unit = request.POST.get('unit', '')
        if unit != '':
            if Unit.objects.filter(unit_name=unit).exists():
                return render(request, 'add_unit.html',
                              {'user': request.session['user'], 'message': f"'{unit}' already exists"})
            Unit.objects.create(unit_name=unit)
            return redirect(unit_table)
    return render(request, 'add_unit.html', {'notification': notification_list, 'user': request.session['user']})


def spare_parts_table(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    parts = SparePart.objects.all()
    linked_content = []
    for content in parts:
        linked_content.append(content.__dict__)
    print(linked_content)
    return render(request, 'spare_parts_tables.html', {'notification': notification_list, 'data': linked_content, 'user': request.session['user']})


def add_spare_part(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
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
            return render(request, 'add_spare_parts.html',
                          {'data': linked_content, 'user': request.session['user'], 'message': message})
    return render(request, 'add_spare_parts.html', {'notification': notification_list, 'data': linked_content, 'user': request.session['user']})


def purchase(request):
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications_unread = auth_user.notifications.unread()
    for item in list(notifications_unread):
        notification_list.append(str(item))
    if 'user' not in request.session:
        return redirect('login')
    purchase = Purchase.objects.all()
    linked_content = []
    for content in purchase:
        linked_content.append(content.__dict__)

    return render(request, 'purchase.html',
                  {'notification': notification_list, 'data': linked_content,
                   'user': request.session['user']})


def purchase_parts(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
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
                        Purchase.objects.create(supplier=supplier, challan_no=challan, parts_id=parts_id,
                                                quantity=quantity, box=box, created_at=date)
                    except:
                        print('error creating purchase')
                    check += 1
                count += 1
                if check == val:
                    break
                if count > 50:
                    break
        except:
            print('error in val')
            return redirect(purchase_parts)
        while True:
            break
        print(val)
    return render(request, 'purchase_spare_parts.html', {'notification': notification_list, 'data': linked_content, 'user': request.session['user']})


def get_unit_stock(request):
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
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
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    args = Product.objects.filter()
    maxProductNo = args.aggregate(Max('product_no')).get('product_no__max')
    if maxProductNo is None:
        maxProductNo = 1
    product_barcode_list = []
    all = []
    for i in range(maxProductNo):
        if Product.objects.filter(product_no=i + 1).exists():
            product = list(
                Product.objects.filter(product_no=i+1).values_list("product_name", "product_barcode", "parts_name",
                                                                     "parts_quantity", "parts_unit", "status", "product_id",))
            parts = []
            for item in range(len(product)):
                thisdict = {
                    'parts_name': product[item][2],
                    'quantity': product[item][3],
                    'unit': product[item][4],
                }
                parts.append(thisdict)
            custom_dict = {
                'product_id': product[0][6],
                'product_name': product[0][0],
                'barcode': product[0][1],
                'parts_list': parts,
                'status': product[0][5],
            }
            code39 = barcode.get('code39', product[0][1], writer=ImageWriter())
            code39.save('code39')
            with open("code39.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            barcode_dict = {
                'product_name': product[0][0],
                'barcode': product[0][1],
                'barcode_img': encoded_string.decode("utf-8")
            }
            product_barcode_list.append(barcode_dict)
            all.append(custom_dict)
    print(product_barcode_list)
    open_status = []
    for i in range(maxProductNo):
        if Product.objects.filter(product_no=i + 1).exists():
            product = list(
                Product.objects.filter(product_no=i+1).values_list("product_name", "product_barcode", "parts_name",
                                                                     "parts_quantity", "parts_unit", "status", "product_id",))
            if product[0][5] == 'Open Status':
                parts = []
                for item in range(len(product)):
                    thisdict = {
                        'parts_name': product[item][2],
                        'quantity': product[item][3],
                        'unit': product[item][4],
                    }
                    parts.append(thisdict)
                custom_dict = {
                    'product_id': product[0][6],
                    'product_name': product[0][0],
                    'barcode': product[0][1],
                    'parts_list': parts,
                    'status': product[0][5],
                }
                open_status.append(custom_dict)

    in_progress = []
    for i in range(maxProductNo):
        if Product.objects.filter(product_no=i + 1).exists():
            product = list(
                Product.objects.filter(product_no=i + 1).values_list("product_name", "product_barcode", "parts_name",
                                                                     "parts_quantity", "parts_unit", "status",
                                                                     "product_id", ))
            if product[0][5] == 'In Progress':
                parts = []
                for item in range(len(product)):
                    thisdict = {
                        'parts_name': product[item][2],
                        'quantity': product[item][3],
                        'unit': product[item][4],
                    }
                    parts.append(thisdict)
                custom_dict = {
                    'product_id': product[0][6],
                    'product_name': product[0][0],
                    'barcode': product[0][1],
                    'parts_list': parts,
                    'status': product[0][5],
                }
                in_progress.append(custom_dict)
    completed = []
    for i in range(maxProductNo):
        if Product.objects.filter(product_no=i + 1).exists():
            product = list(
                Product.objects.filter(product_no=i + 1).values_list("product_name", "product_barcode", "parts_name",
                                                                     "parts_quantity", "parts_unit", "status",
                                                                     "product_id", ))
            if product[0][5] == 'Completed':
                parts = []
                for item in range(len(product)):
                    thisdict = {
                        'parts_name': product[item][2],
                        'quantity': product[item][3],
                        'unit': product[item][4],
                    }
                    parts.append(thisdict)
                custom_dict = {
                    'product_id': product[0][6],
                    'product_name': product[0][0],
                    'barcode': product[0][1],
                    'parts_list': parts,
                    'status': product[0][5],
                }
                completed.append(custom_dict)

    return render(request, 'product.html', {
        'notification': notification_list,
        'all': all,
        'open_status': open_status,
        'in_progress': in_progress,
        'completed': completed,
        'barcode': product_barcode_list,
        'user': request.session['user']})


def create_product(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    linked_content = []
    parts = SparePart.objects.all()
    for content in parts:
        linked_content.append(content.__dict__)
    if request.method == "POST":
        try:
            val = int(request.POST.get('total', ''))
            count = 1
            check = 0
            check_list = []
            flag = False
            args = Product.objects.filter()
            maxProductNo = args.aggregate(Max('product_no')).get('product_no__max')
            if maxProductNo is None:
                maxProductNo = 1
            while 1:
                name = request.POST.get('name_' + str(count), '')
                product_id = request.POST.get('product_id_' + str(count), '')
                if product_id is '':
                    print('empty')
                    count += 1
                    continue
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
                print(partsname, parts_id, quantity)
                if partsname != '' and parts_id != '' and quantity != '':

                    parts_id = int(parts_id)
                    quantity = int(quantity)
                    qry = SparePart.objects.filter(parts_id=parts_id).values_list('quantity')
                    qry_list = list(qry)
                    current_quantity = qry_list[0][0]
                    if current_quantity is None:
                        current_quantity = 1
                    if quantity > current_quantity:
                        pass
                    print(product_id, unit, name, parts_invoice, barcode, partsname, parts_id, parts_box, quantity,
                          store, comment, date, parts_date, product_quantity, product_invoice)
                    if not flag:
                        available_product_parts = list(
                            Product.objects.filter(parts_id=parts_id, parts_quantity=quantity).values_list(
                                'product_id'))
                        for item in available_product_parts:
                            check_list.append(item[0])
                    if flag:
                        print('hit to create')
                        Product.objects.create(product_no=maxProductNo+1, product_id=product_id, parts_unit=unit, product_name=name,
                                               parts_invoice=parts_invoice,
                                               product_barcode=barcode, parts_name=partsname, parts_id=parts_id,
                                               parts_box=parts_box,
                                               parts_quantity=quantity, product_store=store, product_comment=comment,
                                               product_quantity=product_quantity, product_invoice=product_invoice)
                    check += 1
                count += 1
                if check == val:
                    for item in check_list:
                        if check_list.count(item) == val:
                            if Product.objects.filter(product_id=item).count() == val:
                                return HttpResponse("402")
                    check = 0
                    count = 1
                    if flag:
                        user = User.objects.all()
                        notify.send(auth_user, recipient=user, verb=', created a product')
                        subject = 'New Product has been Created'
                        message = f'Product ID: {product_id}'
                        email_from = settings.EMAIL_HOST_USER
                        email_object_list = list(EmailSettings.objects.all().values('email_name'))
                        recipient_list = []
                        for item in email_object_list:
                            recipient_list.append(item.get('email_name'))
                        v = send_mail(subject, message, email_from, recipient_list)
                        print('hit by product created')
                        return HttpResponse("Product Created")
                    flag = True

        except:
            print('error')
            notify.send(auth_user, recipient=user, verb=', created a product')
            return redirect(create_product)

    else:
        return render(request, 'create_product.html', {'notification': notification_list, 'data': linked_content, 'user': request.session['user']})


def change_product_status(request):
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    current = request.GET['current'].split(']')
    print(current)
    product_id = current[0]
    current_status = current[1]
    update_status = request.GET['update']
    if current_status == 'Open':
        current_status = 'Open Status'
    elif current_status == 'Manufacture':
        current_status = 'In Progress'
    elif current_status == 'Complete':
        current_status = 'Completed'

    if update_status == 'Open':
        update_status = 'Open Status'
    elif update_status == 'Manufacture':
        update_status = 'In Progress'
    elif update_status == 'Complete':
        update_status = 'Completed'

    if current_status == update_status:
        return HttpResponse('Select different status!')

    if current_status == 'Open Status' and update_status == 'Completed':
        return HttpResponse('Need to choose Manufacture status first!')

    if current_status == 'In Progress' and update_status == 'Open Status':
        return HttpResponse('Open Status can not applicable here!')

    if current_status == 'Completed' and update_status == 'Open Status':
        return HttpResponse('Product already created!')

    if current_status == 'Completed' and update_status == 'In Progress':
        return HttpResponse('Product already created!')

    if current_status == 'Open Status' and update_status == 'In Progress':
        product_list = list(Product.objects.filter(product_id=product_id).values_list('parts_id', 'parts_quantity'))

        for parts in product_list:
            parts_quantity = list(SparePart.objects.filter(parts_id=int(parts[0])).values_list('quantity'))
            if parts_quantity[0][0] is None:
                return HttpResponse('Spare parts quantity is not enough!')
            if parts_quantity[0][0] < parts[1]:
                return HttpResponse('Spare parts quantity is not enough!')

        for parts in product_list:
            parts_quantity = list(SparePart.objects.filter(parts_id=int(parts[0])).values_list('quantity'))
            SparePart.objects.filter(parts_id=int(parts[0])).update(quantity=parts_quantity[0][0] - parts[1])

        Product.objects.filter(product_id=product_id).update(status=update_status)

    if current_status == 'In Progress' and update_status == 'Completed':
        Product.objects.filter(product_id=product_id).update(status=update_status)

    return HttpResponse('Status Updated!')


def mark_notification_read(request):
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    qs = auth_user.notifications.unread()
    qs.mark_all_as_read(auth_user)
    print('hit')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def product_tabel(request):
    return render(request, 'tables.html', {})


def all_notification(request):
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    all_notification_list = []
    notifications_unread = auth_user.notifications.unread()
    notifications_read = auth_user.notifications.read()

    for item in list(notifications_unread):
        all_notification_list.append(str(item))
    for item in list(notifications_read):
        all_notification_list.append(str(item))

    return render(request, 'notifications.html', {'data': all_notification_list})


def email_settings(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    email = EmailSettings.objects.all()
    linked_content = []
    for content in email:
        linked_content.append(content.__dict__)
    return render(request, 'email.html',
                  {'notification': notification_list, 'data': linked_content, 'user': request.session['user']})


def add_email(request):
    if 'user' not in request.session:
        return redirect('login')
    user = request.session['user']
    auth_user = User.objects.get(username=user)
    notification_list = []
    notifications = auth_user.notifications.unread()
    for item in list(notifications):
        notification_list.append(str(item))
    if request.POST:
        email = request.POST.get('name', '')
        print(email)
        if email != '':
            if EmailSettings.objects.filter(email_name=email).exists():
                return render(request, 'add_email.html',
                              {'user': request.session['user'], 'message': f"'{email}' already exists"})
            EmailSettings.objects.create(email_name=email)
            return redirect(email_settings)
    return render(request, 'add_email.html', {'notification': notification_list, 'user': request.session['user']})
