from django.urls import path
from .views import register, user_login, user_logout, add_measurement, add_fabric, create_order, dashboard, fabric_list, order_list, update_order_status, measurement_list

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add-measurement/', add_measurement, name='add_measurement'),
    path('measurements/', measurement_list, name='measurement_list'),
    path('add-fabric/', add_fabric, name='add_fabric'),
    path('fabric-list/', fabric_list, name='fabric_list'), 
    path('create-order/', create_order, name='create_order'),
    path('dashboard/', dashboard, name='dashboard'),
     path('create-order/', create_order, name='create_order'),
    path('order-list/', order_list, name='order_list'),
    path('update-order/<int:order_id>/', update_order_status, name='update_order'),
]
