# barbershop\urls.py
from django.contrib import admin
from django.urls import path
from core.views import landing, thanks, orders_list, order_details, test_template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing),
    path('thanks/', thanks),
    path('orders/', orders_list),
    path('orders/<int:order_id>/', order_details),
    path("test_template/", test_template)
]