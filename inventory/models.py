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
        base_cost = sum([mi_ingredient.cost for mi_ingredient in self.menuitemingredient_set.all()])
        try:
            markup_percentage = BusinessConfig.objects.first().markup_percentage
        except AttributeError:  # In case no configuration has been set
            markup_percentage = settings.MENU_ITEM_MARKUP_PERCENTAGE  # The default value from settings
        
        markup = base_cost * (markup_percentage / 100)
        return base_cost + markup
    
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
    date_time = models.DateTimeField(default=datetime.now)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Check ingredient availability for each order item
        for order_item in self.orderitem_set.all():
            order_item.check_ingredient_availability()

        # Update total_cost based on OrderItems
        self.total_cost = sum([oi.cost for oi in self.orderitem_set.all()])
        
        super(Order, self).save(*args, **kwargs)


    # Deduct used ingredients from stock
        for mi_ingredient in self.menu_item.menuitemingredient_set.all():
            ingredient = mi_ingredient.ingredient
            required_quantity = mi_ingredient.quantity_required * self.quantity
            ingredient.quantity -= required_quantity
            ingredient.save()

        self.total_cost = self.menu_item.cost * self.quantity
        super(Order, self).save(*args, **kwargs)


class BusinessConfig(models.Model):
    markup_percentage = models.PositiveIntegerField(default=50, help_text="Markup percentage for menu items.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Business Configurations"

    def __str__(self):
        return "Business Configuration"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def cost(self):
        return self.menu_item.price * self.quantity
    def check_ingredient_availability(self):
        for mi_ingredient in self.menu_item.menuitemingredient_set.all():
            ingredient = mi_ingredient.ingredient
            required_quantity = mi_ingredient.quantity_required * self.quantity
            if ingredient.quantity < required_quantity:
                raise ValueError(f"Not enough {ingredient.name} for {self.menu_item.name}")