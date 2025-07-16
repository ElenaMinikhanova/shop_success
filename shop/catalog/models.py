from django.db import models

# Create your models here.
class Catalog(models.Model):
    CATEGORY_CHOICES = [
        ('Цветы', 'Цветы'),
        ('Семена', 'Семена'),
        ('Игрушки', 'Игрушки'),
        ('Разное', 'Разное'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фотография')