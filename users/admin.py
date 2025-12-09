from django.contrib import admin

from catalog.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass