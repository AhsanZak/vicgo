from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from . models import *
from app1.models import Order, OrderItem, Coupon, CancelledOrder
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import FileSystemStorage

# Create your views here.


def admin_panel(request):
    if request.session.has_key('password'):
        no_users = User.objects.count()
        x = 1000
        no_order = Order.objects.count()
        no_product = ProductDetail.objects.count()

        order = Order.objects.filter(date_ordered__range=['2020-10-01', '2030-01-01'])
        order_dict = {}
        # for x in order:
        #     if not x.transaction_id in order_dict.keys():
        #         order_dict[x.transaction_id] = x
        total_sales = 0
        dict2 = {}
        total_amount = 0

        for date, items in order_dict.items():
            if not items.date_ordered in dict2.keys():
                dict2[items.date_ordered] = {'price': items.total_price}
                total_amount += items.total_price
            else:
                dict2[items.date_ordered]['price'] += items.total_price
                total_amount += items.total_price

        return render(request, 'AdminPanel/index.html',
                      {'no_users': no_users, 'x': x, 'no_order': no_order, 'no_product': no_product,
                       'total_revenue': total_amount})
    else:
        return redirect('/admin-login')


def admin_login(request):
    if request.session.has_key('password'):
        return redirect('/adminpanel')

    if request.method == 'POST':
        us = request.POST.get('username')
        ps = request.POST.get('password')

        if us == 'admin' and ps == '12345':
            request.session['password'] = ps
            return redirect(admin_panel)
        else:
            return render(request, 'AdminPanel/login.html')

    else:
        return render(request, 'AdminPanel/login.html')


def dashboard(request):
    return redirect('/admin-login')


def admin_logout(request):
    if request.session.has_key('password'):
        request.session.flush()
    return redirect('admin_login')


def manage_user(request):
    if request.session.has_key('password'):
        details = User.objects.all().order_by('id')
        return render(request, 'AdminPanel/users.html', {'user': details})
    else:
        return redirect('/admin-login')


def create_user(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            first_name = request.POST['first_name']
            email = request.POST['email']
            username = request.POST['username']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            mobile_no = request.POST['mobileNo']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username Taken")
                    return render(request, 'AdminPanel/signup.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, "Email Taken")
                    return render(request, 'AdminPanel/signup.html')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name)
                    UserDetail.objects.create(mobile_no=mobile_no, user=user)
                    user.save()
                    return redirect('/manage-user')
            else:
                messages.info(request, "Passwords Not Matching")
                return render(request, 'AdminPanel/signup.html', )

        else:
            return render(request, 'AdminPanel/signup.html')
    else:
        return redirect('/admin-login')


def delete_user(request, user_id):
    if request.session.has_key('password'):
        User.objects.get(id=user_id).delete()
        return redirect('/manage-user')
    else:
        return redirect('/admin-login')


def update_user(request, user_id):
    if request.session.has_key('password'):
        user = User.objects.filter(id=user_id).first
        return render(request, 'AdminPanel/update.html', {'user': user})
    else:
        return redirect('/admin-login')


def edit_user(request, user_id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            user = User.objects.get(id=user_id)
            user.first_name = request.POST['full_name']
            user.email = request.POST['email']
            user.username = request.POST['username']
            user.last_name = request.POST['mobileNo']

            user.save()

            return redirect('/manage-user')
        else:
            return HttpResponse("Say Hello to the Error")
    else:
        return redirect('/admin-login')


def block_user(request, user_id):
    if request.session.has_key('password'):
        user = User.objects.get(id=user_id)
        if user.is_active == True:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('/manage-user')
    else:
        return redirect('/admin-login')


def manage_coupon(request):
    if request.session.has_key('password'):
        coupon = Coupon.objects.all()
        return render(request, 'AdminPanel/manage_coupon.html', {'coupon': coupon})
    else:
        return redirect(admin_login)


def add_coupon(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            name = request.POST.get('name')
            validity_start = request.POST.get('validity_start')
            validity_end = request.POST.get('validity_end')
            discount = request.POST.get('discount')

            Coupon.objects.create(name=name, status=True, validity_start=validity_start, 
                            validity_end=validity_end, discount=discount)
            return redirect(manage_coupon)
        else:
            return render(request, 'AdminPanel/add_coupon.html')
    else:
        return redirect(admin_login)


def edit_coupon(request, id):
    if request.session.has_key('password'):
        coupon = Coupon.objects.get(id=id)
        if request.method == 'POST':
            coupon.name = request.POST.get('name')
            coupon.status = request.POST.get('status')
            coupon.validity_start = request.POST.get('validity_start')
            coupon.validity_end = request.POST.get('validity_end')
            coupon.discount = request.POST.get('discount')

            coupon.save()
            return redirect(manage_coupon)
        else:
            return render(request, 'AdminPanel/edit_coupon.html', {'coupon': coupon})
    else:
        return redirect(admin_login)


def delete_coupon(request, id):
    if request.session.has_key('password'):
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
        return redirect(manage_coupon)
    else:
        return redirect(admin_login)


def manage_refferal(request):
    if request.session.has_key('password'):
        refferal = RefferalOffer.objects.all()
        return render(request, 'AdminPanel/manage_refferal.html', {'reffral': refferal})

    else:
        return render(request, 'admin/login.html')


def edit_refferal(request, id):
    if request.session.has_key('password'):
        reff = RefferalOffer.objects.get(id=id)
        if request.method == 'POST':
            reff.reff_name = request.POST.get('offer_name')
            reff.refferd_person_discount = request.POST.get('person_discount')
            reff.order_maximum = request.POST.get('minimum_price')
            reff_offer_type = request.POST.get('offer_type')
            print(reff_offer_type)
            if reff_offer_type == "price":
                reff.reff_price = request.POST.get('offer_price')
                reff.reff_offer_type = reff_offer_type
            elif reff_offer_type == "percentage":
                reff.reff_discount = request.POST.get('offer_discount')
                reff.reff_offer_type = reff_offer_type
            reff.save()
            return redirect('manage_refferal')
        else:
            return render(request, "AdminPanel/edit_refferal.html", {"reff": reff})
    else:
        return redirect(admin_login)


def add_refferal(request):
    if request.session.has_key('password'):
        reff = RefferalOffer()
        if request.method == 'POST':
            reff.reff_name = request.POST.get('offer_name')
            reff.reffered_person_discount = request.POST.get('person_discount')
            reff.order_maximum = request.POST.get('minimum_price')
            reff_offer_type = request.POST.get('offer_type')
            print(reff_offer_type)
            if reff_offer_type == "price":
                reff.reff_price = request.POST.get('offer_price')
                reff.reff_offer_type = reff_offer_type
            elif reff_offer_type == "percentage":
                reff.reff_discount = request.POST.get('offer_discount')
                reff.reff_offer_type = reff_offer_type
            reff.save()
            return redirect('manage_refferal')
        else:
            return render(request, "AdminPanel/add_refferal.html")
    else:
        return redirect(admin_login)


def delete_refferal(request, id):
    if request.session.has_key('password'):
        reff = RefferalOffer.objects.get(id=id)
        reff.delete()
        return redirect(manage_refferal)
    else:
        return redirect(admin_login)


def delete_product(request, product_id):
    if request.session.has_key('password'):
        ProductDetail.objects.get(id=product_id).delete()
        return redirect('/manage-product')
    else:
        return redirect('/admin-login')


def manage_product(request):
    if request.session.has_key('password'):
        details = ProductDetail.objects.all().order_by('id')
        return render(request, 'AdminPanel/products.html', {'details': details})
    else:
        return redirect('/admin-login')


def update_product(request, product_id):
    if request.session.has_key('password'):
        product = ProductDetail.objects.filter(id=product_id).first()
        return render(request, 'AdminPanel/update-product.html', {'product': product})
    else:
        return redirect('/admin-login')


def edit_product(request, product_id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            product = ProductDetail.objects.get(id=product_id)
            product.product_name = request.POST['product_name']
            product.product_category = Category.objects.get(category_name=request.POST['product_category'])
            product.product_price = request.POST['product_price']
            product.product_description = request.POST['product_description']
            if 'imageInput' not in request.POST:
                product_image = request.FILES.get('imageInput')
            else:
                product_image = product.product_image
            product.product_image = product_image
            product.save()

            return redirect('/manage-product')
        else:
            return HttpResponse("Say Hello to the Error")
    else:
        return redirect('/admin-login')


def create_product(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            product_name = request.POST['product_name']
            product_category = Category.objects.get(category_name=request.POST['product_category'])
            product_description = request.POST['product_description']
            product_price = request.POST['product_price']
            image_data = request.POST['pro_img']
            extra_images = request.FILES.getlist('file[]')

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=product_name + '.' + ext)

            product = ProductDetail.objects.create(product_name=product_name, product_category=product_category,
                                                   product_description=product_description, product_price=product_price,
                                                   product_image=data)
            product.save()

            for img in extra_images:
                fs=FileSystemStorage()
                file_path=fs.save(img.name,img)
                fileurl = fs.url(file_path)
                pimage=ProductImages.objects.create(product=product,extra_images=file_path)
                pimage.save()

            return redirect('/manage-product')
        else:
            category = Category.objects.all()
            return render(request, 'AdminPanel/trial_CreateProduct.html', {'category': category})
    else:
        return redirect('/admin-login')


def manage_category(request):
    value = Category.objects.all().order_by('id')
    return render(request, 'AdminPanel/category_management.html', {'value': value})


def update_category(request, id):
    if request.session.has_key('password'):
        category = Category.objects.get(id=id)
        return render(request, 'AdminPanel/edit_category.html', {'category': category})
    else:
        return redirect(admin_login)


def edit_category(request, id):
    if request.session.has_key('password'):
        if request.method == 'POST':
            category = Category.objects.get(id=id)
            category.category_name = request.POST['category']
            category.category_image = request.FILES['category_image']
            category.save()
            return redirect(manage_category)
        else:
            return render(request, 'AdminPanel/edit_category.html')
    else:
        return redirect(admin_login)


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        category_image = request.FILES['category_image']
        Category.objects.create(category_name=category_name, category_image=category_image)
        return redirect(manage_category)
    else:
        return render(request, 'AdminPanel/add_category.html')


def delete_category(request, id):
    b = Category.objects.get(id=id)
    b.delete()
    messages.info(request, 'Deleted Successfully')
    return redirect(manage_category)


def manage_order(request):
    if request.session.has_key('password'):
        order = Order.objects.all()
        order_dict = {}
        for x in order:
            if not x.transaction_id in order_dict.keys():
                order_dict[x.transaction_id] = x
        return render(request, 'AdminPanel/manage_order.html', {'table_data': order_dict})
    else:
        return redirect(admin_login)


def cancel_order(request, tid):
    if request.session.has_key('password'):
        object = Order.objects.filter(transaction_id=tid)
        for x in object:
            # if x.order_status == 'Cancelled':
            #     x.order_status = 'Placed'
            if x.order_status == 'Placed':
                x.order_status = 'Cancelled'
        x.save()
        return redirect(manage_order)
    else:
        return redirect(admin_login)


def order_report(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        total_order = Order.objects.filter(date_ordered__range=[start_date, end_date]).count()

        order = Order.objects.filter(date_ordered__range=[start_date, end_date])
        order_dict = {}
        for x in order:
            if not x.transaction_id in order_dict.keys():
                order_dict[x.transaction_id] = x
        total_sales = 0
        dict2 = {}
        total_amount = 0

        for date, items in order_dict.items():
            if not items.date_ordered in dict2.keys():
                dict2[items.date_ordered] = {'price': items.total_price}
                total_amount += items.total_price
            else:
                dict2[items.date_ordered]['price'] += items.total_price
                total_amount += items.total_price

        return render(request, 'AdminPanel/order_report.html', {'total_order': total_order, 'table_data': order_dict,
                                                     'total_sales': dict2, 'total_amount': total_amount})
    else:
        start_date = '2020-10-1'
        end_date = '2030-01-01'
        total_order = Order.objects.filter(date_ordered__range=[start_date, end_date]).count()

        order = Order.objects.filter(date_ordered__range=[start_date, end_date])
        order_dict = {}
        for x in order:
            if not x.transaction_id in order_dict.keys():
                order_dict[x.transaction_id] = x
        total_sales = 0
        dict2 = {}
        total_amount = 0

        for date, items in order_dict.items():
            if not items.date_ordered in dict2.keys():
                dict2[items.date_ordered] = {'price': items.total_price}
                total_amount += items.total_price
            else:
                dict2[items.date_ordered]['price'] += items.total_price
                total_amount += items.total_price

        return render(request, 'AdminPanel/order_report.html', {'total_order': total_order,
                                                     'table_data': order_dict, 'total_sales': dict2,
                                                     'total_amount': total_amount})


def manage_offer(request):
    if request.session.has_key('password'):
        offer = Offer.objects.all()
        return render(request, 'AdminPanel/manage_offer.html', {'offers': offer})
    else:
        return redirect(admin_login)


def add_offer(request):
    if request.session.has_key('password'):
        categories = Category.objects.all()
        products = ProductDetail.objects.all()

        if request.method == 'POST':
            offer_type = request.POST['offer_type']
            offer_name = request.POST['offer_name']        
            category_id = request.POST['category']
            product_id = request.POST['product']
            discount_percentage = int(request.POST['discount_amount'])
            offer_starts = request.POST['offer_start']
            offer_ends = request.POST['offer_ends']
            product = ProductDetail.objects.get(id=product_id)
            if offer_type == 'single':
                real_price = product.product_price
                product.offer_price = real_price
                product.product_price =  real_price - (real_price * discount_percentage/100)
                product.offer_percentage = discount_percentage
                product.save()
                Offer.objects.create(offer_name=offer_name,product=product,discount_amount=discount_percentage,offer_start=offer_starts,
                                    offer_expiry=offer_ends,offer_type=offer_type)
            else:
                category = Category.objects.get(id=category_id)
                products = ProductDetail.objects.filter(product_category=category)
                for product in products:
                    real_price = product.product_price
                    product.offer_price = real_price
                    product.product_price = real_price - (real_price * discount_percentage/100)
                    product.offer_percentage = discount_percentage
                    product.save()
                Offer.objects.create(offer_name=offer_name,product=product,category=category,discount_amount=discount_percentage,
                                    offer_start=offer_starts,offer_expiry=offer_ends,offer_type=offer_type)
            return redirect(manage_offer)
        else:
            context = {'categories':categories, 'products':products }
            return render(request, 'AdminPanel/add_offer.html', context)
    else:
        return redirect(admin_login)


def delete_offer(request, id):
    if request.user.is_authenticated:
        offers = Offer.objects.get(id=id)
        if offers.offer_type == 'single':
            product_id = offers.product.id
            product = ProductDetail.objects.get(id=product_id)

            offer_price = product.product_price
            real_price = product.offer_price

            product.price = real_price
            product.offer_price = 0
            product.save()
            offers.delete()
        else:
            category_id = offers.category
            category = Category.objects.get(id=category_id.id)
            products = ProductDetail.objects.filter(product_category=category)
            for product in products:
                offer_price = product.product_price
                real_price = product.offer_price
                product.price = real_price
                product.offer_price = 0
                product.save()
            offers.delete()
        return redirect(manage_offer)
    else:
        return redirect(admin_login)


def pending_order(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            pending = Order.objects.filter(date_ordered__range=[start_date, end_date], order_status='Pending')
            order_dict = {}
            for x in pending:
                if not x.transaction_id in order_dict.keys():
                    order_dict[x.transaction_id] = x
            pending = Order.objects.filter(order_status='Pending').count()
            return render(request, 'AdminPanel/pending_order.html', {'table_data': order_dict, 'pending': pending})
        else:
            pending = Order.objects.filter(order_status='Pending').count()
            return render(request, 'AdminPanel/pending_order.html', {'pending': pending})
    else:
        return redirect(admin_login)


def placed_order(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            placed = Order.objects.filter(date_ordered__range=[start_date, end_date], order_status='Placed')
            order_dict = {}
            for x in placed:
                if not x.transaction_id in order_dict.keys():
                    order_dict[x.transaction_id] = x
            placed = Order.objects.filter(order_status='Placed').count()
            return render(request, 'AdminPanel/placed_orders.html', {'table_data': order_dict, 'placed': placed})
        else:
            placed = Order.objects.all()
            order_dict = {}
            for x in placed:
                if not x.transaction_id in order_dict.keys():
                    order_dict[x.transaction_id] = x
            placed = Order.objects.filter(order_status='Placed').count()
            return render(request, 'AdminPanel/placed_orders.html', {'table_data': order_dict, 'placed': placed})
    else:
        return redirect(admin_login)


def cancelled_order(request):
    if request.session.has_key('password'):
        if request.method == 'POST':
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            cancelled = CancelledOrder.objects.filter(date_ordered__range=[start_date, end_date], order_status='Cancelled')
            order_dict = {}
            for x in cancelled:
                if not x.transaction_id in order_dict.keys():
                    order_dict[x.transaction_id] = x
            cancelled = CancelledOrder.objects.filter(order_status='Cancelled').count()
            return render(request, 'AdminPanel/cancelled_orders.html', {'table_data': order_dict, 'cancelled': cancelled})
        else:
            cancelled = CancelledOrder.objects.all()
            order_dict = {}
            for x in cancelled:
                if not x.transaction_id in order_dict.keys():
                    order_dict[x.transaction_id] = x
            cancelled = CancelledOrder.objects.filter(order_status='Cancelled').count()
            return render(request, 'AdminPanel/cancelled_orders.html', {'table_data': order_dict, 'cancelled': cancelled})
    else:
        return redirect(admin_login)


def product_return(request):
    if request.session.has_key('password'):
        cancel_order = CancelledOrder.objects.all()
        cancel_order_dict = {}
        for x in cancel_order:
            if not x.transaction_id in cancel_order_dict.keys():
                cancel_order_dict[x.transaction_id] = x
                cancel_order_dict[x.transaction_id].order_price = cancel_order_dict[x.transaction_id].total_price
            else:
                cancel_order_dict[x.transaction_id].order_price += cancel_order_dict[x.transaction_id].total_price

        return render(request, 'AdminPanel/return_and_refunds.html', {'cancel_order': cancel_order_dict})
    else:
        return redirect(admin_login)


def approve_refund(request, id):
    if request.session.has_key('password'):
        cancel_order = CancelledOrder.objects.filter(id=id)
        for x in cancel_order:
            total_price = x.total_price
            user = x.user
            x.refund = True
            x.save()
        user = UserDetail.objects.get(user=user)
        user.wallet += total_price
        user.save()
        return redirect(product_return)
    else:
        return redirect(admin_login)