from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):
    """Заказ"""

    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    stripe_token = models.CharField(max_length=100)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_IN_PROGRESS
    )

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):
    """Заказаннйы товар"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id