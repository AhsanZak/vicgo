from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('single/<int:product_id>', views.single, name="single"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('otp-login/', views.otp_login, name="otp_login"),
    path('user-profile/', views.user_profile, name="user_profile"),
    path('user-setprofile/', views.edit_user_profile, name="edit_userProfile"),

    path('category-item/<int:item_id>/', views.category_item, name="category_item"),

    path('add-cart/<int:id>/', views.add_cart, name="add_cart"),
    path('cart', views.cart, name="cart"),
    path('cart/update/<int:id>', views.cart_update, name="cart_update"),
    path('wallet/<int:id>/', views.wallet, name="wallet"),
    path('apply-coupon/', views.apply_coupon, name="apply_coupon"),

    path('user-removeOrderItem/<int:id>', views.user_remove_order_item, name="user_removeOrderItem"),
    path('add-address', views.add_address, name="add_address"),
    path('user-payment/<int:id>', views.user_payment, name="user_payment"),
    path('success-razorpay/', views.success_razorpay, name="success_razorpay"),
    path('success-paypal/', views.success_paypal, name="success_paypal"),


    path('view-order/', views.view_order, name="view_order"),
    path('order-items/', views.order_items, name="order_items"),
    path('cancel-order/<str:id>/', views.cancel_order_user, name="cancel_order_user"),

]
