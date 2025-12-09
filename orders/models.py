from django.contrib.auth.models import User
from django.db import models
from products.models import Product

ORDER_STATUS_CHOICES = [
    ('new', 'Новый'),
    ('paid', 'Оплачено'),
    ('confirmed', 'Подтверждено'),
    ('delivered', 'Доставлен'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField("Имя", max_length=50)
    phone = models.CharField("Телефон", max_length=20)
    address = models.CharField("Адрес", max_length=255, blank=True)
    delivery_type = models.CharField("Тип", max_length=10, choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')])
    total_price = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=ORDER_STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Время", auto_now_add=True)
    telegram_username = models.CharField("Telegram", max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Заказ #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Количество", default=1)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
