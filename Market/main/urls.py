from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('order/<int:order_id>/', show_order, name='show_order'),
    path('makeorder/', make_order, name='make_order'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('my_orders_list/', my_orders_list, name='my_orders_list'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('orders_list/', orders_list, name='orders_list'),
    path('order_check/<int:order_id>/', order_check, name='order_check'),
    path('logout/', logout_user, name='logout'),
    path('delete_status/<int:status_id>/', delete_status, name='delete_status'),
]