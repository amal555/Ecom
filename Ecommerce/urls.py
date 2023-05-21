from django.urls import path
from . import views
from .views import ProductTable ,CustomerTable
urlpatterns = [
    path('',views.home,name='home'),
    path('create_user',views.create_user,name='create_user'),
    path('user_login',views.user_login,name='user_login'),
    path('homepage',views.dashboard,name='homepage'),
    path('add_products',views.add_products,name='add_products'),
    path('add_product_details',views.add_product_details,name='add_product_details'),
    path('dashboard',views.dashboard,name='dashboard'),
    path("product_details_tb/", ProductTable.as_view()),
    path("update_status",views.update_status,name='update_status'),
    path("customers_dashboard",views.customers_dashboard,name='customers_dashboard'),
    path("customer_tb_details/",CustomerTable.as_view()),
    path("add_customers",views.add_customers,name='add_customers'),
    path("add_customer_details",views.add_customer_details,name='add_customer_details'),
    path("delete_customer",views.delete_customer,name='delete_customer'),
    path("edit_customer",views.edit_customer,name='edit_customer'),
    path("update_customer",views.update_customer,name='update_customer'),
]
