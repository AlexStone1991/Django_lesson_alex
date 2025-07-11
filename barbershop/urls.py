# barbershop\urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core.views import landing, thanks, orders_list, order_detail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='main'),
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders'),
    path('orders/<int:order_id>/', order_detail, name='order_details'),
]

# Добавляем статуку и медиа ЕСЛИ в режиме разработчика
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])