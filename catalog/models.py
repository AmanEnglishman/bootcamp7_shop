from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.parent.name})'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def product_image_upload_path(instance, filename):
    # красивый путь: /products/<product_id>/<filename>
    return f'products/{instance.product.id}/{filename}'


class Product(models.Model):
    article = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    made_country = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)  # 0–100

    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def final_price(self):
        """Цена после скидки"""
        if self.discount_percent:
            return self.price - (self.price * self.discount_percent / 100)
        return self.price

    def __str__(self):
        return f'{self.title} ({self.article})'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_upload_path)

    def __str__(self):
        return f'Image for {self.product.title}'


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.key}: {self.value}'

'catalog/models.py'
'catalog/admin.py'

'python manage.py makemigrations'
'python manage.py migrate'