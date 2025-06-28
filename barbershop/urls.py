# barbershop\urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core.views import landing, thanks, orders_list, order_details


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('thanks/', thanks),
    path('orders/', orders_list),
    path('orders/<int:order_id>/', order_details),
]

# Добавляем статуку и медиа ЕСЛИ в режиме разработчика
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])