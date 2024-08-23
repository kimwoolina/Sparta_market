from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# 해시태그 기능
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)  # 해시태그는 유일해야 함

    def __str__(self):
        return self.name

    def clean(self):
        # 해시태그는 띄어쓰기와 특수문자를 포함할 수 없음
        if ' ' in self.name or any(char in self.name for char in "#@!$%^&*()"):
            raise ValidationError("해시태그는 띄어쓰기와 특수문자를 포함할 수 없습니다.")


class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True)
    view_cnt = models.PositiveIntegerField(default=0)  # 조회수

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products"
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_products"
    )

    # 해시 태그
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)

    def __str__(self):
        return self.title
    
    # 조회수 증가
    def increment_view_cnt(self):
        # Increase the view count by 1
        self.view_cnt += 1
        self.save()


    # 저장할 때 게시물에 중복된 해시태그가 없도록 확인  
    def save(self, *args, **kwargs):
        # Save the product before running clean
        super().save(*args, **kwargs)

        # Check for duplicate tags
        if len(self.tags.all()) != len(set(self.tags.all())):
            raise ValidationError("게시물에 중복된 해시태그를 설정할 수 없습니다.")



class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    
