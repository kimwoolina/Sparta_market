from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import F, FloatField, ExpressionWrapper, Count


def index(request):
    return render(request, "products/index.html")


def products(request):
    products = Product.objects.all().order_by("-pk")
    context = {
        "products": products,
    }
    return render(request, "products/products.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    product.increment_view_cnt()  # 조회수 증가

    like_count = product.like_users.count()  # count likes

    comment_form = CommentForm()
    comments = product.comments.all().order_by("-pk")

    context = {
        "product": product,
        "like_count": like_count,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "products/product_detail.html", context)


# 정렬
def product_list(request):
    sort_by = request.GET.get('sort', 'latest')
    
    if sort_by == 'popular':
        # 조회수(view_cnt)와 좋아요(like_users.count())를 50%씩 반영하여 가중 평균을 계산
        products = Product.objects.annotate(
            likes_count=Count('like_users'),  # 좋아요 수 계산
            popularity=ExpressionWrapper(
                (F('view_cnt') * 0.5 + F('likes_count') * 0.5),
                output_field=FloatField()
            )
        ).order_by('-popularity')  # 인기순으로 정렬
    else:
        products = Product.objects.order_by('-created_at')  # 최신순으로 정렬

    context = {
        'products': products,
        'sort_by': sort_by  # 정렬 기준을 컨텍스트에 추가
    }

    return render(request, 'products/product_list.html', context)


@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "products/create.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.author != request.user:
        if request.method == "POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                product = form.save()
                return redirect("products:product_detail", product.pk)
        else:
            form = ProductForm(instance=product)
    else:
        return redirect("products:products")

    context = {
        "form": form,
        "product": product,
    }
    return render(request, "products/update.html", context)


@require_POST
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        if product.author == request.user:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
    return redirect("products:products")


@require_POST
def comment_create(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
        return redirect("products:product_detail", product.pk)


@require_POST
def comment_delete(request, pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user:
            comment.delete()
    return redirect("products:product_detail", pk)


@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)  # 좋아요 취소
        else:
            product.like_users.add(request.user)  # 좋아요
        return redirect("products:products")
    return redirect("accounts:login")
