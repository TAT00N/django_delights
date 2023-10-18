from django.contrib import admin


# Register your models here.

from django.contrib import admin
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase

# Admin for Ingredient
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price_per_unit')
    search_fields = ('name',)

# Inline Admin for RecipeRequirement (This will allow editing of ingredients required for each menu item directly from the MenuItem form)
class RecipeRequirementInline(admin.TabularInline):
    model = RecipeRequirement
    extra = 1

# Admin for MenuItem
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name', 'description')
    inlines = [RecipeRequirementInline]

# Admin for Purchase
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'quantity', 'purchase_time', 'total_cost', 'total_revenue', 'profit')
    list_filter = ('purchase_time', 'menu_item')
    search_fields = ('menu_item__name',)

# Registering the models with their admin views
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
