from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, Comment
from .forms import ProductForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Count
from django.db.models import Q


def index(request):
    products = Product.objects.all().order_by("-pk")
    context = {
        "products": products,
    }
    return render(request, "products/products.html", context)


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
        products = Product.objects.annotate(
            likes_count=Count('like_users')
        ).order_by('-likes_count', '-view_cnt')
    else:
        products = Product.objects.order_by('-created_at')
    
    context = {
        'products': products,
        'sort_by': sort_by
    }

    return render(request, 'products/products.html', context)


@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            tags = form.cleaned_data['tags']
            product.tags.set(tags)  # ManyToManyField에 태그 설정
            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "products/create.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Check if the current user is the author of the product
    if product.author != request.user:
        return redirect("products:products")  # Redirect if the user is not the author

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:product_detail", product.pk)
    else:
        form = ProductForm(instance=product)

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

# 상세 페이지에서 좋아요
@require_POST
def detail_like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)  # 좋아요 취소
        else:
            product.like_users.add(request.user)  # 좋아요
        return redirect("products:product_detail", pk=product.pk)  # pk를 포함하여 리다이렉트
    return redirect("accounts:login")


# 검색
def search(request):
    form = SearchForm(request.GET or None)
    products = Product.objects.none()  # 기본적으로 빈 쿼리셋
    
    if form.is_valid():
        query = form.cleaned_data['query']
        # 검색 로직
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'form': form,
        'products': products,
        'search_query': form.cleaned_data['query'] if form.is_valid() else ''
    }
    return render(request, 'products/products.html', context)