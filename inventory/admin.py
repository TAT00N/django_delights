from django.contrib import admin
from .models import Ingredient, MenuItem, MenuItemIngredient, Purchase
# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'price_per_unit')
    search_fields = ['name']

class MenuItemIngredientInline(admin.TabularInline):
    model = MenuItemIngredient
    extra = 1

class MenuItemAdmin(admin.ModelAdmin):
    inlines = [MenuItemIngredientInline]

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Purchase)
admin.site.register(MenuItem, MenuItemAdmin)
