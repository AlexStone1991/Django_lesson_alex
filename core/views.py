# core/views.py
from django.shortcuts import render, HttpResponse
from .data import orders, services, masters
from django.db.models import Q

def landing(request):
    """
    Отвечает за маршрут '/'
    """
    return render(request, 'landing.html')

def thanks(request):
    """
    Отвечает за маршрут  '/thanks/'
    """
    context = {
        "test_var": "Привет с базового шаблона"
    }
    return render(request, 'thanks.html', context=context)

def orders_list(request):
    """
    Отвечает за маршрут /orders/'
    """
    context = {
        "orders": orders,
    }
    return render(request, 'orders_list.html', context=context)

def order_details(request, order_id):
    """
    Отвечает за маршрут /orders/<int:order_id>/
    :param request: HttpRequest
    :param order_id: int (номер заказа)
    """
    order = [order for order in orders if order['id'] == order_id]
    try:
        order = order[0]
        context = {
            "order": order,
            "my_fariable": "Hello, world",
        }
    except IndexError:
        return HttpResponse(f'<h1>Заказ {order_id} не найден</h1>')
    else:
        
        return render(request, 'order_details.html', context=context)

# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def say_my_name(self):
#         return f"Меня зовут {self.name}"
    
#     def __str__(self):
#         return f"Это метод __str__: {self.name}"

# test_list = ["Алевтина", "Бородач", "Гендальф Серый", "Лысый из Игры Престолов"]
# test_dict = {
#     "master": "Алевтина",
#     "age": 25,
#     "is_master": True
# }
# test_person = Person("Лысый из Игры Престолов", 50)

# def test_template(request):
#     """
#     Отвечает за маршрут /test_template/
#     """
#     context_data = {
#         "variable_1": "Значение переменной 1",
#         "test_list": test_list,
#         "test_dict": test_dict,
#         "test_person": test_person,
#     }
#     return render(request, 'test_template.html', context=context_data)

