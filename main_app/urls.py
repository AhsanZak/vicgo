from django.urls import path
from . import views

urlpatterns = [
    path('adminpanel/', views.admin_panel, name="admin_panel"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    path('manage-user/', views.manage_user, name='manage_user'),
    path('manage-product/', views.manage_product, name='manage_product'),
    path('manage-category/', views.manage_category, name="manage_category"),

    path('manage-order/', views.manage_order, name="manage_order"),
    path('cancel-order/<str:tid>', views.cancel_order, name="cancel_order"),
    path('order-report', views.order_report, name="order_report"),
    path('cancelled-order', views.cancelled_order, name="cancelled_order"),
    path('pending-order', views.pending_order, name="pending_order"),
    path('placed_order', views.placed_order, name="placed_order"),

    path('add-category', views.add_category, name="add_category"),
    path('delete-category/<int:id>', views.delete_category, name="delete_category"),
    path('update-category/<int:id>', views.update_category, name="update_category"),
    path('edit-category/<int:id>', views.edit_category, name="edit_category"),

    path('manage-coupon', views.manage_coupon, name="manage_coupon"),
    path('add-coupon', views.add_coupon, name="add_coupon"),
    path('delete-coupon/<int:id>', views.delete_coupon, name="delete_coupon"),
    path('edit-coupon/<int:id>', views.edit_coupon, name="edit_coupon"),

    path('manage-refferal/', views.manage_refferal, name="manage_refferal"),
    path('add-refferal/', views.add_refferal, name="add_refferal"),
    path('edit-refferal/<int:id>/', views.edit_refferal, name="edit_refferal"),
    path('delete-refferal/<int:id>/', views.delete_refferal, name="delete_refferal"),

    path('manage-offer/', views.manage_offer, name="manage_offer"),
    path('add-offer/', views.add_offer, name="add_offer"),
    path('delete-offer/<int:id>', views.delete_offer, name="delete_offer"),

    path('delete-user/<int:user_id>', views.delete_user, name='delete_user'),
    path('delete-product/<int:product_id>', views.delete_product, name='delete_product'),
    path('update-user/<int:user_id>', views.update_user, name='update_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('block-user/<int:user_id>/', views.block_user, name='block_user'),

    path('update-product/<int:product_id>', views.update_product, name='update_product'),
    path('edit-product/<int:product_id>', views.edit_product, name='edit_product'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_product/', views.create_product, name='create_product'),

    path('product_return/', views.product_return, name="product_return"),
    path('approve_refund/<int:id>', views.approve_refund, name="approve_refund")

]

