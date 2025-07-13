from django.contrib import admin
from .models import Master, Order, Service
from django.db.models import Q, Count, Sum, QuerySet

admin.site.register(Master)
# admin.site.register(Order)
admin.site.register(Service)

# делаем фильтр для OrderAdmin total_price
class TotalOrderPrice(admin.SimpleListFilter):
    title = "По общей сумме заказа"
    parameter_name = "total_order_price"

    def lookups(self, request, model_admin):
        "Возвращают варианты фильтра"
        return (
            ("one_thousend", "До тысячи"),
            ("three_thousend", "До трех тысяч"),
            ("five_thousend", "До пяти тысяч"),
            ("up_five_thousend", "Свыше пяти тысяч"),
        )
    
    def queryset(self, request, queryset):
        """
        Возвращает данные в зависимости от нажатой кнопки фильтра
        """
        queryset = queryset.annotate(total_price_agg=Sum("services__price"))
        
        if self.value() == "one_thousend":
            return queryset.filter(total_price_agg__lt=1000)
        if self.value() == "three_thousend":
            return queryset.filter(total_price_agg__gte=1000, total_price_agg__lt=5000)
        if self.value() == "five_thousend":
            return queryset.filter(total_price_agg__gte=3000, total_price_agg__lt=5000)
        if self.value() == "up_five_thousend":
            return queryset.filter(total_price_agg__gte=5000)
        
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # отображение полей в списке заказов
    list_display = (
        "name",
        "phone",
        "master",
        "date_created",
        "appointment_date",
        "status",
        "total_price",
        "total_income",
    )
    # поисковая форма
    search_fields = ("name", "phone", "status")

    # фильтры
    list_filter = ("status", "master", "services", TotalOrderPrice)

    # сколько записей на странице
    list_per_page = 3

    # Кликабельные ссылки на записи
    list_display_links = ("phone", "name",)

    # поля, которые можно редактировать
    list_editable = ("status",)

    # Не редактируемые поля
    readonly_fields = ("date_created", "date_updated",)

    # Регестрация действий
    actions = ("mark_completed", "mark_canceled", "mark_new", "mark_confirmed")
    # Кастомное действие отметить заявки как comleted - Завершена

    @admin.action(description="Отметить как завершенные")
    def mark_completed(self, request, queryset):
        queryset.update(status="completed")

    @admin.action(description="Отметить как отмененная")
    def mark_canceled(self, request, queryset):
        queryset.update(status="canceled")

    @admin.action(description="Отметить как новая")
    def mark_new(self, request, queryset):
        queryset.update(status="new")

    @admin.action(description="Отметить как подтвержденная")
    def mark_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    # Кастомный столбец с общей суммой M2M services
    @admin.display(description="Общая сумма")
    def total_price(self, obj):
        return sum([service.price for service in obj.services.all()])

    # # Кастомный столбец сколько нам принес этот номер телефона сумма всех услуг всех заказов этого номера со статусом completed
    @admin.display(description="Выручка")
    def total_income(self, obj):
        # Найти все заявки сделанные с этим номером телефона + статус завершенно и жадно выгрузить все услуги
        orders = Order.objects.filter(phone=obj.phone, status="completed").prefetch_related("services")
        # Суммировать все цены услуг
        return sum([service.price for order in orders for service in order.services.all()])