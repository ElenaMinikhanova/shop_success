from django.db import models

# Create your models here.
class Catalog(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/')
    like = models.BooleanField(default=False)