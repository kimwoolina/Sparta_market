from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from products.models import Product
from django.db.models import F, FloatField, ExpressionWrapper

def users(request):
    return render(request, "users/users.html")


def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    
    # 사용자가 등록한 물품 수
    products_cnt = member.products.count()
    
    # 사용자가 좋아요를 누른 물품 수
    liked_products_cnt = member.like_products.count()

    context = {
        "member": member,
        "products_count": products_cnt,
        "liked_products_count": liked_products_cnt,
    }
    return render(request, "users/profile.html", context)



@require_POST
def follow(request, user_id):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if member != request.user:
            if member.user_followers.filter(pk=request.user.pk).exists():
                member.user_followers.remove(request.user)
            else:
                member.user_followers.add(request.user)
        return redirect("users:profile", username=member.username)
    return redirect("accounts:login")


# 사용자가 등록한 물품 목록
def user_products(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    products = member.products.all()
    context = {
        'products': products,
        'page_title': f"{member.username}님의 매물목록",
        'username': member.username,
        #'page_type': 'product',
    }
    return render(request, 'users/products.html', context)


# 사용자가 좋아요를 누른 물품 목록
def user_liked_products(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    liked_products = member.like_products.all()
    context = {
        'products': liked_products,
        'page_title': f"{member.username}님의 관심목록",
        'username': member.username,
        #'page_type': 'liked',
    }
    return render(request, 'users/products.html', context)


# 유저 페이지에서 찜
@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
        else:
            product.like_users.add(request.user)

        next_url = request.POST.get('next', 'users:user_products')
        return redirect(next_url)
    return redirect("accounts:login")