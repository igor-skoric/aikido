from django.contrib import admin
from .models import Instructor, Blog, Image, Product, Category, Config
from django.contrib.contenttypes.admin import GenericTabularInline


class ImageInline(GenericTabularInline):
    model = Image
    extra = 1


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Instructor)
admin.site.register(Category)
admin.site.register(Config)