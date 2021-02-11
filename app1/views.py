from django.shortcuts import render, redirect
from main_app.models import ProductDetail, Category, UserDetail
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import OrderItem, Order, ShippingAddress
from django.http import JsonResponse
import uuid
import datetime
import base64
from django.core.files.base import ContentFile


# Create your views here.

def home(request):
    products = ProductDetail.objects.all()
    category = Category.objects.all()
    if request.user.is_authenticated:
        return render(request, 'User/index.html', {'products': products, 'category': category, 'user': request.user})
    else:
        return render(request, 'User/index.html', {'products': products, 'category': category})


def category_item(request, item_id):
    if request.user.is_authenticated:
        category_items = Category.objects.get(id=item_id)
        products = ProductDetail.objects.filter(product_category=category_items.id)
        category = Category.objects.all()

        return render(request, 'User/index.html', {'products': products, 'category': category, 'user': request.user})
    else:
        return redirect(login)


def single(request, product_id):
    product = ProductDetail.objects.get(id=product_id)
    category_product = ProductDetail.objects.filter(product_category=product.product_category)
    return render(request, 'User/single.html', {'product': product, 'category_product': category_product})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.filter(username=username).first()
        if user is not None and check_password(password, user.password):
            if user.is_active == False:
                messages.info(request, 'User is Blocked')
            else:
                auth.login(request, user)
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
        print("loogeed out")
        auth.logout(request)
        return redirect(home)
    else:
        return redirect(home)


def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        profilepic = UserDetail.objects.get(user=user)
        return render(request, 'User/userProfile.html', {'username': user.username, 'profilepic': profilepic})
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
        return render(request, 'User/cart.html', {'cart_data': cart, 'total_amount': get_total, 'address': address})
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
    pass


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

            if ShippingAddress.objects.filter(address=address).exists():
                return redirect(add_address)
            else:
                address = ShippingAddress.objects.create(user=user, address=address, state=state, city=city)
                address.save()
                return redirect(add_address)
        else:
            return redirect(cart)
    else:
        return redirect(home)


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
            for x in orderItem:
                get_total = x.get_total + get_total

            return render(request, 'User/payment.html',
                          {'address': address, 'items': orderItem, 'total_price': get_total})
    else:
        user = request.user
        cart = OrderItem.objects.filter(user=user)
        return render(request, 'User/checkout.html')



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

        return render(request, 'User/order.html', {'item_data': order_dict}, )
    return redirect(login)

def order_items(request):
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(user=user)
        return render(request, 'User/orderItems.html', {'orders': order})
