from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage

class User(AbstractUser):
    # 팔로우 관계 설정
    followings = models.ManyToManyField(
        'self', 
        related_name='user_followers',  # 역참조 이름을 'user_followers'로 설정
        symmetrical=False
    )

    followers = models.ManyToManyField(
        'self', 
        related_name='user_followings',  # 역참조 이름을 'user_followings'로 설정
        symmetrical=False
    )

    # 프로필 이미지
    profile_image = models.ImageField(
        upload_to='images/profile_images/',  # 프로필 이미지가 저장될 디렉토리
        null=True,  # 이미지가 없어도 허용
        blank=True,  # 관리자 폼에서 필수 입력이 아님
        default='images/default/default_profile_image.png'  # 기본 이미지의 경로
    )

    # 프로필 이미지를 변경할 때 기존 프로필 사진 파일 삭제
    def save(self, *args, **kwargs):
        if self.pk:  # 사용자가 이미 존재하는지 확인
            old_user = User.objects.get(pk=self.pk)
            if old_user.profile_image and old_user.profile_image != self.profile_image:
                # 기본 이미지는 삭제하지 않도록 확인
                if old_user.profile_image.name != 'images/default/default_profile_image.png':
                    if default_storage.exists(old_user.profile_image.name):
                        default_storage.delete(old_user.profile_image.name)

        super(User, self).save(*args, **kwargs)
