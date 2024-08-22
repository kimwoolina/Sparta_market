from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.products, name="products"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path('', views.product_list, name='product_list'),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path(
        "<int:pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path("<int:pk>/like/", views.like, name="like"),
    path("index/", views.index, name="index"),
]
