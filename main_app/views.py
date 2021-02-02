from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse

# Create your views here.


def admin_panel(request):
    if request.session.has_key('password'):
        no_users = User.objects.count()
        x = 1000
        no_order = Order.objects.count()
        no_product = ProductDetail.objects.count()

        order = Order.objects.filter(date_ordered__range=['2020-10-01', '2030-01-01'])
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

        return render(request, 'index.html',
                      {'no_users': no_users, 'x': x, 'no_order': no_order, 'no_product': no_product,
                       'total_revenue': total_amount})
    else:
        return redirect('/admin-login')
