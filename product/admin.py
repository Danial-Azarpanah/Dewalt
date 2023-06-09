from django.contrib import admin
from .models import *


class SpecAdmin(admin.StackedInline):
    model = Spec


class PictureAdmin(admin.TabularInline):
    model = Picture


class AdditionalItemAdmin(admin.TabularInline):
    model = AdditionalItems


class FeatureAdmin(admin.TabularInline):
    model = Features


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_price', 'discount', 'get_discounted_price_admin')
    list_filter = ('created_at', 'call_before')
    search_fields = ('title', 'id', 'price')
    inlines = [FeatureAdmin, PictureAdmin, SpecAdmin, AdditionalItemAdmin]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "show_image")


admin.site.register(Favorite)
admin.site.register(Comparison)
admin.site.register(Comment)
admin.site.register(DiscountCode)

