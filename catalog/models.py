from django.db import models
from random import randint
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f'{self.name} - {self.parent.name}'

def product_image_upload_path(instance, filename):
    return f'catalog/images/{instance.product.title}/{filename}'

class Images(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path)

    def __str__(self):
        return f'{self.product.name} - {self.image.id}'

class Specification(models.Model):
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='specifications')
    specification = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.product.name} - {self.specification}'


class Products(models.Model):
    article = models.PositiveIntegerField(default=randint(0, 999999999), unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    title = models.CharField(max_length=255)
    make_county = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
