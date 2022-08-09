from django.contrib import admin

# Register your models here.
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class AttributeValueINnLine(admin.TabularInline):

    model = AttributeValue
    extra = 0


@admin.register(ProductAttribute)
class ProductAttribute(admin.ModelAdmin):
    inlines = [AttributeValueINnLine]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AttributeValueINnLine]


admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(RatingStar)
admin.site.register(Rating)