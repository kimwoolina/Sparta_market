from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model


def users(request):
    return render(request, "users/users.html")


def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    context = {
        "member": member,
    }
    return render(request, "users/profile.html", context)


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
