from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.core.files.storage import default_storage

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

    # 프로필 이미지를 변경할 때 기존 프로필 사진 파일 삭제
    def save(self, *args, **kwargs):
        # 이전 프로필 이미지가 존재하고 새로운 이미지로 교체된 경우 삭제
        if self.pk:
            old_user = User.objects.get(pk=self.pk)
            if old_user.profile_image and old_user.profile_image != self.profile_image:
                if default_storage.exists(old_user.profile_image.name):
                    default_storage.delete(old_user.profile_image.name)

        super(User, self).save(*args, **kwargs)
