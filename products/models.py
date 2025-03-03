from django.db import models
import django.core.validators

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    rating = models.FloatField(validators=[
        django.core.validators.MinValueValidator(0),
        django.core.validators.MaxValueValidator(5)
    ],null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title