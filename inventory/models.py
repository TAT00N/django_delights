from django.db import models

# Ingredients in Inventory
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Current quantity in stock
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

# Restaurant Menu Items
class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Selling price to the customers
    image_link = models.URLField(blank=True, null=True)  # Optional link to an image or recipe
    
    def __str__(self):
        return self.name

# Ingredients required for each menu item
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Quantity of ingredient required for the menu item

    class Meta:
        unique_together = ['menu_item', 'ingredient']

# Purchase Log
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Number of menu items bought in this purchase
    purchase_time = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        # The cost to the restaurant for making the menu item
        return sum([req.ingredient.price_per_unit * req.quantity for req in self.menu_item.reciperequirement_set.all()]) * self.quantity
    
    @property
    def total_revenue(self):
        # The revenue from selling the menu item
        return self.menu_item.price * self.quantity
    
    @property
    def profit(self):
        return self.total_revenue - self.total_cost

    @property
    def total_revenue(self):
        return self.menu_item.price * self.quantity

    @classmethod
    def overall_revenue(cls):
        return sum(purchase.total_revenue for purchase in cls.objects.all())

    @classmethod
    def overall_cost(cls):
        return sum(purchase.total_cost for purchase in cls.objects.all())

    @classmethod
    def overall_profit(cls):
        return cls.overall_revenue() - cls.overall_cost()