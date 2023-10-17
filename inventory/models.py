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
    def price(self):
        return sum([mi.cost for mi in self.menuitemingredient_set.all()])
    
class MenuItemIngredient(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('menu_item', 'ingredient')
    @property
    def cost(self):
        return self.ingredient.price_per_unit * self.quantity_required
      
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_time = models.DateTimeField(default=datetime.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_cost = self.menu_item.price_per_unit * self.quantity
        super(Purchase, self).save(*args, **kwargs)

#At the moment this should be reviewed. 
