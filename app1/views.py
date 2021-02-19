from django.shortcuts import render, redirect
from main_app.models import ProductDetail, Category, UserDetail
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import OrderItem, Order, ShippingAddress, CancelledOrder, Coupon, ProductImages
from django.http import JsonResponse
import uuid
import datetime
import base64
from django.core.files.base import ContentFile
import requests
import json



# Create your views here.

def home(request):
    products = ProductDetail.objects.all()
    category = Category.objects.all()
    if request.user.is_authenticated:
        user_detail = UserDetail.objects.filter(user=request.user)
        return render(request, 'User/index.html', {'products': products, 'category': category, 'user': request.user, 'user_detail':user_detail})
    else:
        return render(request, 'User/index.html', {'products': products, 'category': category})


def category_item(request, item_id):
    if request.user.is_authenticated:
        category_items = Category.objects.get(id=item_id)
        products = ProductDetail.objects.filter(product_category=category_items.id)
        category = Category.objects.all()
        user_detail = UserDetail.objects.get(user=request.user)

        return render(request, 'User/index.html', {'products': products, 'category': category, 'user': request.user, 'user_detail':user_detail})
    else:
        return redirect(login)


def single(request, product_id):
    product = ProductDetail.objects.get(id=product_id)
    category_product = ProductDetail.objects.filter(product_category=product.product_category)
    user_detail = UserDetail.objects.get(user=request.user)
    product_images = ProductImages.objects.filter(product=product)
    context = {
        'product': product, 'category_product': category_product, 'user_detail':user_detail, 
        'product_images': product_images
    }
    return render(request, 'User/single.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user is not None and check_password(password, user.password):
            if user.is_active == False:
                messages.info(request, 'User is Blocked')
            else:
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(home)
        else:
            messages.info(request, "Invalid Credentials")
            return redirect(login)
    else:
        return render(request, 'User/login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        email = request.POST['email']
        username = request.POST['username']
        last_name = request.POST['last_name']
        mobile_no = request.POST['mobile_no']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Taken")
                return render(request, 'User/signup.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return render(request, 'User/signup.html')
            elif UserDetail.objects.filter(mobile_no=mobile_no).exists():
                messages.info(request, "Mobile No. already registered")
                return render(request, 'User/signup.html')
            else:
                user = User.objects.create_user(username=username, password=password1, first_name=first_name,
                                                last_name=last_name, email=email)
                UserDetail.objects.create(user=user, mobile_no=mobile_no)
                user.save()
                return redirect('login')
        else:
            messages.info(request, "Passwords Not Matching")
            return render(request, 'User/signup.html')
    else:
        return render(request, 'User/signup.html')


def wallet(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        pass
    else:
        return redirect(login)


def reffral_signup(request, reff_code):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        dic = {"lastname": lastname, "email": email, "username": username}

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Mobile number already taken')
            return render(request, 'refferal_signup.html', dic)

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email is Taken')
            return render(request, 'refferal_signup.html', dic)

        else:
            letter = string.ascii_letters
            result = ''.join(random.choice(letter) for i in range(8))
            if reff_code == "":
                user = User.objects.create_user(last_name=lastname, username=username, email=email, password=password)
                user.save()
            else:
                if Customer.objects.filter(reff_code=reff_code).exists():
                    user = User.objects.create_user(last_name=lastname, username=username, email=email,
                                                    password=password)
                    user.save()
                    cust = Customer.objects.get(reff_code=reff_code)
                    customer, created = Customer.objects.get_or_create(user=user, name=username, email=email,
                                                                       reff_code=result, refferd_user=cust.user_id)
                    messages.info(request, 'User Created')
                    return redirect('login')
                else:
                    messages.info(request, 'Wrong refferel code ')
                    return render(request, 'refferal_signup.html', dic)
            return redirect('login')
    else:
        return render(request, 'refferal_signup.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(home)


def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        profilepic = UserDetail.objects.get(user=user)
        user_detail = UserDetail.objects.get(user=request.user)
        return render(request, 'User/userProfile.html', {'username': user.username, 'profilepic': profilepic, 'user_detail':user_detail})
    else:
        return redirect(login)


def edit_user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            user.first_name = request.POST['full_name']
            user.email = request.POST['email']
            user.last_name = request.POST['mobileNo']

            user_detail = UserDetail.objects.get(user=user)
            if 'imageInput' not in request.POST:
                user_image = request.FILES.get('imageInput')
            else:
                user_image = user_detail.user_image

            user_detail.user_image = user_image
            user_detail.save()
            user.save()
            return redirect(user_profile)

    else:
        return redirect(login)


def add_cart(request, id):
    if request.user.is_authenticated:
        user = request.user
        product = ProductDetail.objects.get(id=id)

        if OrderItem.objects.filter(product=product, user=user).exists():
            order = OrderItem.objects.get(product=product, user=user)
            order.quantity += 1
            order.save()
        else:
            quantity = 1
            OrderItem.objects.create(user=user, product=product, quantity=quantity)
        return redirect(home)
    else:
        return redirect(login)


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        for i in cart:
            i.total_price = i.product.product_price * i.quantity
        get_total = 0
        for x in cart:
            get_total = x.get_total + get_total
        address = ShippingAddress.objects.filter(user=user)
        user_detail = UserDetail.objects.get(user=user)

        context = {
            'cart_data': cart, 'total_amount': get_total, 'address': address, 'user_detail':user_detail
        }
        return render(request, 'User/cart.html', context)
    else:
        return redirect(home)


def cart_update(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            action = request.POST['action']
            if action == 'add':
                carts = OrderItem.objects.filter(user=user)
                cart = OrderItem.objects.get(id=id)
                cart.quantity += 1
                cart.save()
                product_total = cart.product.product_price * cart.quantity
                get_total = 0
                for x in carts:
                    get_total = x.get_total + get_total
                return JsonResponse({'product_total': product_total, 'grand_total': get_total}, safe=False)
            elif action == 'minus':
                carts = OrderItem.objects.filter(user=user)
                cart = OrderItem.objects.get(id=id)
                cart.quantity -= 1
                cart.save()
                product_total = cart.product.product_price * cart.quantity
                get_total = 0
                for x in carts:
                    get_total = x.get_total + get_total
                return JsonResponse({'product_total': product_total, 'grand_total': get_total}, safe=False)


def otp_login(request):
    if request.user.is_authenticated:
        return redirect(home)
    otp = 1
    if request.method == 'POST':
        number = request.POST['mobile']
        request.session['number'] = number
        if UserDetail.objects.filter(mobile_no=number).exists():
            otp = 0
            url = "https://d7networks.com/api/verifier/send"
            number = str(91) + number
            payload = {
                'mobile': number,
                'sender_id': 'SMSINFO',
                'message': 'Your otp code is {code}',
                'expiry': '900'}
            files = [
            ]
            headers = {
                'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
            }
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            data = response.text.encode('utf8')
            datadict = json.loads(data)
            id = datadict['otp_id']
            request.session['id'] = id

            return render(request, 'User/otplogin.html', {'otp': otp})
        else:
            messages.info(request, "Please enter registered Number")
            return render(request, 'User/otplogin.html', {'otp': otp})
    else:
        return render(request, 'User/otplogin.html', {'otp': otp})


def verify_otp(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            otp = request.POST['otp']
            id_otp = request.session['id']
            url = "https://d7networks.com/api/verifier/verify"
            payload = {'otp_id': id_otp,
                       'otp_code': otp}
            files = [

            ]
            headers = {
                'Authorization': 'Token b76a52adeb253e2dbb98dd2378d542f8d53fbe6b'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            data = response.text.encode('utf8')
            datadict = json.loads(data)
            status = datadict['status']

            if status == 'success':
                number = request.session['number']
                user_detail = UserDetail.objects.filter(mobile_no=number).first()
                user = user_detail.user
                print(user)
                if user_detail is not None:
                    if user_detail.user.is_active == False:
                        messages.info(request, 'User is blocked')
                        return redirect(login)

                    else:
                        auth.login(request, user)
                        return redirect(home)
                else:
                    return redirect(login)

            else:
                messages.error(request, 'User not Exist')
                return redirect(login)

        else:
            return HttpResponse("Oops")


def user_remove_order_item(request, id):
    b = OrderItem.objects.get(id=id)
    b.delete()
    return redirect(cart)


def add_address(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            address = request.POST['address']
            state = request.POST['state']
            city = request.POST['city']

            if ShippingAddress.objects.filter(user=user, address=address).exists():
                return redirect(add_address)
            else:
                address = ShippingAddress.objects.create(user=user, address=address, state=state, city=city)
                address.save()
                return redirect(add_address)
        else:
            return redirect(cart)
    else:
        return redirect(home)


def apply_coupon(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.session.has_key('coupon'):
                return JsonResponse('active', safe=False)
            user = request.user
            name = request.POST['coupenCode']
            total_amount = float(request.POST['total_amount'])

            if Coupon.objects.filter(name=name).exists():
                coupon = Coupon.objects.get(name=name)
                discount = coupon.discount
                coupon_session = request.session['coupon'] = discount
                discounted_price = total_amount - (total_amount*discount)/100
                print(discounted_price)
                return JsonResponse({'result': 'validcoupen', 'amount': discounted_price}, safe=False)
            else:
                return JsonResponse('notvalidcoupen', safe=False)

            
    else:
        return redirect(login)


def user_payment(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            mode = request.POST['mode']
            transaction_id = uuid.uuid4()
            if mode == 'Paypal':
                return JsonResponse({'mode': mode, 'tid': transaction_id}, safe=False)
            elif mode == 'Razorpay':
                return JsonResponse({'mode': mode, 'tid': transaction_id}, safe=False)

            else:
                date = datetime.datetime.now()
                address = ShippingAddress.objects.get(id=id)
                cart = OrderItem.objects.filter(user=user)
                get_total = 0

                if request.session.has_key('coupon'):
                    discount = request.session['coupon']
                    for x in cart:
                        get_total = x.get_total + get_total
                    get_total = get_total - (get_total*discount)/100
                    for item in cart:
                        Order.objects.create(user=user, address=address, product=item.product,
                                            total_price=get_total,
                                            transaction_id=transaction_id, date_ordered=date, payment_status='Pending',
                                            payment_mode=mode, quantity=0, order_status='Placed')
                    cart.delete()
                    del request.session['coupon']
                    return JsonResponse({'mode': mode, 'tid': transaction_id}, safe=False)
                else:
                    for x in cart:
                        get_total = x.get_total + get_total
                    for item in cart:
                        Order.objects.create(user=user, address=address, product=item.product,
                                            total_price=get_total,
                                            transaction_id=transaction_id, date_ordered=date, payment_status='Pending',
                                            payment_mode=mode, quantity=0, order_status='Placed')
                    cart.delete()
                    return JsonResponse({'mode': mode, 'tid': transaction_id}, safe=False)
        else:
            user = request.user
            address = ShippingAddress.objects.get(id=id)
            orderItem = OrderItem.objects.filter(user=user)
            get_total = 0
            user_detail = UserDetail.objects.get(user=request.user) 

            if request.session.has_key('coupon'):
                discount = request.session['coupon']
                for x in orderItem:
                    get_total = x.get_total + get_total
                get_total = get_total - (get_total*discount)/100
                context = {
                    'address': address, 'items': orderItem, 'total_price': get_total, 'user_detail':user_detail, 'coupon_active': "Coupon is active ..!"
                }
                return render(request, 'User/payment.html', context)
            else:
                for x in orderItem:
                    get_total = x.get_total + get_total
                context = {
                    'address': address, 'items': orderItem, 'total_price': get_total, 'user_detail':user_detail
                }
                return render(request, 'User/payment.html', context)
    else:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'User/checkout.html')


def success_razorpay(request):
    if request.user.is_authenticated:
        date = datetime.datetime.now()
        user = request.user
        mode = 'Razorpay'
        id = request.POST['id']
        tid = request.POST['tid']
        address = ShippingAddress.objects.get(id=id)
        cart = OrderItem.objects.filter(user=user)
        get_total = 0

        if request.session.has_key('coupon'):
            discount = request.session['coupon']
            for x in cart:
                get_total = x.get_total + get_total
            get_total = get_total - (get_total*discount)/100
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product, total_price=get_total, transaction_id=tid, 
                date_ordered=date, payment_status='SUCCESS', payment_mode=mode, quantity=item.quantity, order_status='Placed')

            del request.session['coupon']
            cart.delete()
            return JsonResponse('success', safe=False)
        else:
            for x in cart:
                get_total = x.get_total + get_total
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product, total_price=get_total, transaction_id=tid, 
                date_ordered=date, payment_status='SUCCESS', payment_mode=mode, quantity=item.quantity, order_status='Placed')

            cart.delete()
            return JsonResponse('success', safe=False)
    else:
        return redirect(login)


def success_paypal(request):
    if request.user.is_authenticated:
        date = datetime.datetime.now()
        user = request.user
        mode = 'Paypal'
        id = request.POST['id']
        tid = request.POST['tid']
        address = ShippingAddress.objects.get(id=id)
        cart = OrderItem.objects.filter(user=user)
        get_total = 0

        if request.session.has_key('coupon'):
            discount = request.session['coupon']
            for x in cart:
                get_total = x.get_total + get_total
            get_total = get_total - (get_total*discount)/100
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product,
                                    total_price=get_total,
                                    transaction_id=tid, date_ordered=date, payment_status='SUCCESS',
                                    payment_mode=mode, quantity=0, order_status='Placed')
            del request.session['coupon']
            cart.delete()
            return JsonResponse('success', safe=False)

        else:
            for x in cart:
                get_total = x.get_total + get_total
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product,
                                    total_price=get_total,
                                    transaction_id=tid, date_ordered=date, payment_status='SUCCESS',
                                    payment_mode=mode, quantity=0, order_status='Placed')
            cart.delete()
            return JsonResponse('success', safe=False)
    else:
        return redirect(login)

def success_wallet(request):
    if request.user.is_authenticated:
        date = datetime.datetime.now()
        user = request.user
        mode = 'Vicgo Wallet'
        id = request.POST['id']
        tid = request.POST['tid']
        address = ShippingAddress.objects.get(id=id)
        cart = OrderItem.objects.filter(user=user)
        get_total = 0

        if request.session.has_key('coupon'):
            discount = request.session['coupon']
            for x in cart:
                get_total = x.get_total + get_total
            get_total = get_total - (get_total*discount)/100
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product,
                                    total_price=get_total,
                                    transaction_id=tid, date_ordered=date, payment_status='SUCCESS',
                                    payment_mode=mode, quantity=0, order_status='Placed')
            del request.session['coupon']
            cart.delete()
            return JsonResponse('success', safe=False)

        else:
            for x in cart:
                get_total = x.get_total + get_total
            for item in cart:
                Order.objects.create(user=user, address=address, product=item.product,
                                    total_price=get_total,
                                    transaction_id=tid, date_ordered=date, payment_status='SUCCESS',
                                    payment_mode=mode, quantity=0, order_status='Placed')
            cart.delete()
            return JsonResponse('success', safe=False)
    else:
        return redirect(login)


def view_order(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user)
        order_dict = {}
        for x in order:
            if not x.transaction_id in order_dict.keys():
                order_dict[x.transaction_id] = x
                order_dict[x.transaction_id].order_price = order_dict[x.transaction_id].total_price
            else:
                order_dict[x.transaction_id].order_price += order_dict[x.transaction_id].total_price
        print(order_dict)
        user_detail = UserDetail.objects.get(user=request.user)

        cancel_order = CancelledOrder.objects.filter(user=user)
        cancel_order_dict = {}
        for x in cancel_order:
            if not x.transaction_id in cancel_order_dict.keys():
                cancel_order_dict[x.transaction_id] = x
                cancel_order_dict[x.transaction_id].order_price = cancel_order_dict[x.transaction_id].total_price
            else:
                cancel_order_dict[x.transaction_id].order_price += cancel_order_dict[x.transaction_id].total_price


        context = {
            'item_data': order_dict, 'user_detail':user_detail, 'cancel_order': cancel_order_dict
        }
        return render(request, 'User/order.html', context)
    return redirect(login)


def order_items(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user)
        user_detail = UserDetail.objects.get(user=request.user)
        return render(request, 'User/orderItems.html', {'orders': order, 'user_detail':user_detail})
    else:
        redirect(login)


def cancel_order_user(request, id):
    if request.user.is_authenticated:
        order = Order.objects.filter(transaction_id=id)

        for x in order:
            total_price = x.total_price
            CancelledOrder.objects.create(user=request.user, address=x.address, product=x.product,
                                 total_price=x.total_price,
                                 transaction_id=x.transaction_id, date_ordered=x.date_ordered, payment_status=x.payment_status,
                                 payment_mode=x.payment_mode, quantity=0, order_status='Cancelled')
        order.delete()
        return redirect(view_order)

    else:
        return redirect(login)


