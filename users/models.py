from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # изображение пользователя будет сохраняться в папку media
    image = models.ImageField(upload_to='users_image', blank=True)


