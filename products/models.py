import sys
from datetime import datetime, timedelta, time
from datetime import date
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Товар"""
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True)
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    sale = models.IntegerField('Скидка в процентах', blank=True, default=0)
    qty = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created = models.DateField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def product_new(self):
        if self.created + timedelta(days=7) > date.today():
            return True
        else:
            return False

    def get_price(self):
        price = float(self.price * (100 - self.sale) / 100)
        return price

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    """Картинки товара"""
    product = models.ForeignKey(Product,
                                related_name='images',
                                blank=True,
                                null=True,
                                default=None,
                                on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.id

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        new_image = img.convert('RGB')
        resize_new_img = new_image.resize((500, 500), Image.ANTIALIAS)
        filestream = BytesIO()
        resize_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )
        super().save(*args, **kwargs)

    def get_image(self):

        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class ProductAttribute(models.Model):
    """Характеристика"""
    name = models.CharField(max_length=255, verbose_name='Характеристика товара')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class AttributeValue(models.Model):
    """Значение характеристики"""
    value = models.CharField(max_length=255, verbose_name='Значение характеристики товара')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='values', null=True)

    def __str__(self):
        return f"{self.attribute} - {self.product}"

    class Meta:
        verbose_name = "Значение характеристики"
        verbose_name_plural = "Значения характеристик"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="товар",
        related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    product = models.ForeignKey(Product, verbose_name="товар", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

