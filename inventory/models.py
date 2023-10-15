from datetime import datetime
from django.db import models

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_require = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['menu_item', 'ingredients']

    def __str__(self): 
        return f"{self.ingredients.name} for {self.menu_item.name}"
    
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_time = models.DateTimeField(default=datetime.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_cost = self.menu_item.price * self.quantity
        super(Purchase, self).save(*args, **kwargs)

    
