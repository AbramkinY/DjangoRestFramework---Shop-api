from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import *


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ("id",
                  "title",
                  "sale",
                  "get_price",)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ("is_main", "get_image")


class ProductListSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True)
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ("id",
                  "title",
                  "images",
                  "rating_user",
                  "middle_star",
                  "get_absolute_url",
                  "product_new",
                  "description",
                  "sale",
                  "get_price",)


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""

    class Meta:
        model = Review
        fields = ("id", "name", "text")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = ("email", "name", "text", "product")


class AttributeValueSerializer(serializers.ModelSerializer):

    attribute = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = AttributeValue
        fields = ("attribute", "value")


class ProductDetailSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    reviews = ReviewSerializer(many=True)
    images = ProductImageSerializer(many=True)
    values = AttributeValueSerializer(many=True)
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ("id",
                  "title",
                  "category",
                  "images",
                  "description",
                  "values",
                  "reviews",
                  "rating_user",
                  "middle_star",
                  "product_new",
                  "sale",
                  "get_price",
                  )


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "product")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            product=validated_data.get('product', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "get_absolute_url", )


