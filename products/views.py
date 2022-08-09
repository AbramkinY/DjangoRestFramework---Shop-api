from django.db import models
from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .service import get_client_ip

# Create your views here.


class CategoryList(ListAPIView):
    """Список категорий"""
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class LatestProductsList(APIView):
    """Последнее добавленные товары"""

    def get(self, request):
        products = Product.objects.all()[0:4].annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductListView(APIView):
    """Список товаров по категориям"""

    def get(self, request, slug):
        try:
            products = Product.objects.filter(category__slug=self.kwargs.get('slug'), is_active=True).annotate(
                rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
            ).annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            )
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            raise Http404


class ProductDetailView(APIView):
    """Конкретный товар"""

    def get(self, request, category_slug, product_slug):
        try:
            product = Product.objects.filter(category__slug=category_slug, is_active=True).annotate(
                rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
            ).annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            ).get(slug=product_slug)
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            raise Http404


class ReviewCreateView(APIView):
    """Добавление отзыва к товару"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга товару"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class Search(APIView):
    """Поиск"""

    def post(self, request):
        query = request.data.get('query', '')

        if query:
            products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query), is_active=True).annotate(
                rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
            ).annotate(
                middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            )
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({"products": []})

