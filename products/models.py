from django.db import models


# Create your models here.
# модели = таблицы(бд)

class ProductCategory(models.Model):  # категории товаров
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)  # blank-поле может быть пустым

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):  # магический методs
        return self.name


class Product(models.Model):  # описание продукта
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images', blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=64, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # значение с запятой
    quantity = models.PositiveIntegerField(default=0)  # кол-во товаров не может быть отрицательным
    category = models.ForeignKey(ProductCategory,
                                 on_delete=models.CASCADE)  # что происходит с продуктами при удалении категории

    def __str__(self):  # магический метод
        return f'{self.name} | {self.category.name}'
