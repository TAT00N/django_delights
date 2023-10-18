from datetime import datetime
from django.db import models

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, default="Unit") # Example values: "tbsp", "lbs", etc.
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    ingredients = models.ManyToManyField('Ingredient', through='MenuItemIngredient')


    def __str__(self):
        return self.name
    
    @property
    def cost(self):
        return sum([mi_ingredient.cost for mi_ingredient in self.menuitemingredient_set.all()])
    
class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('menu_item', 'ingredient')
    @property
    def cost(self):
        return self.ingredient.price_per_unit * self.quantity_required
      
class Order(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_time = models.DateTimeField(default=datetime.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Compute the total cost for this order
        self.total_cost = self.menu_item.cost * self.quantity

        # Checking for ingredient quantities
        for mi_ingredient in self.menu_item.menuitemingredient_set.all():
            ingredient = mi_ingredient.ingredient
            if ingredient.quantity < (mi_ingredient.quantity_required * self.quantity):  # Multiply by order quantity
                raise ValueError(f"Not enough {ingredient.name} to complete the order")

        # Call the parent class's save method to actually save the order
        super(Order, self).save(*args, **kwargs)


