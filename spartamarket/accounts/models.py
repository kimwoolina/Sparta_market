from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False
    )

    # 프로필 이미지
    profile_image = models.ImageField(
        upload_to='images/profile_images/',  # 사용자 프로필 이미지가 저장될 디렉토리
        null=True,  # 이미지가 없어도 허용
        blank=True,  # 관리자 폼에서 필수 입력이 아님
        default='images/default/default_profile_image.png'  # 디폴트 이미지의 경로
    )
