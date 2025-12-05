from django.contrib import admin
from .models import Category, SubCategory, Products, Specification, Images

class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'article')

    inlines = (ImagesInline, SpecificationInline)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)
    search_fields = ('name',)

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'value', 'specification')

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
