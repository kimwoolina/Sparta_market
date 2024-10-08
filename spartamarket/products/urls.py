from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.products, name="products"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("products/", views.product_list, name="product_list"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path(
        "<int:pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("<int:pk>/like/", views.like, name="like"),
    path("products/<int:pk>/like/", views.detail_like, name="detail_like"),
    path("index/", views.index, name="index"),

    path('search/', views.search, name='search'),
]
