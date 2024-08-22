from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.users, name="users"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path('<str:username>/products/', views.user_products, name='user_products'),
    path('<str:username>/liked-products/', views.user_liked_products, name='user_liked_products'),
    path("<int:pk>/like/", views.like, name="like"),
    path("<int:user_id>/follow/", views.follow, name="follow"),
]
