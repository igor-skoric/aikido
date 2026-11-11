from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    Blog,
    Category,
    Config,
    Image,
    Instructor,
    Location,
    LocationGroup,
    Master,
    Product,
    Program,
    ProgramBelt,
    TimelineEvent,
)


class ImageInline(GenericTabularInline):
    model = Image
    extra = 1


class LocationGroupInline(admin.TabularInline):
    model = LocationGroup
    extra = 1


class ProgramBeltInline(admin.StackedInline):
    model = ProgramBelt
    extra = 0


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Config.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'belt_rank', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    inlines = [LocationGroupInline]


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')
    inlines = [ProgramBeltInline]


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'sort_order', 'is_active')
    list_editable = ('sort_order', 'is_active')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'slug')
    prepopulated_fields = {'slug': ('name',)}
