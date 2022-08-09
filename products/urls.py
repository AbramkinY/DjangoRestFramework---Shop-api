from django.urls import path

from . import views

urlpatterns = [
    path("rating/", views.AddStarRatingView.as_view()),
    path("review/", views.ReviewCreateView.as_view()),
    path("categories/", views.CategoryList.as_view()),
    path('latest-products/', views.LatestProductsList.as_view()),
    path('search/', views.Search.as_view()),
    path("<str:slug>/", views.ProductListView.as_view()),
    path("<slug:category_slug>/<slug:product_slug>/", views.ProductDetailView.as_view()),
    ]


