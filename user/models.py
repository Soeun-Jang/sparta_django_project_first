from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
#장고에서 기본 제공하는 settings 모듈을 가져오는 코드


class UserModel(AbstractUser):

    class Meta:
        db_table = "my_user" # 여기는 테이블 이름이에요! 꼭 기억 해 주세요!

