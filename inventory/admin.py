from django.contrib import admin
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'unit', 'price_per_unit')
    search_fields = ['name']

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MenuItem)
admin.site.register(RecipeRequirement)
admin.site.register(Purchase)