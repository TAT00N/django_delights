from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

@receiver(post_save, sender='inventory.MenuItemIngredient')
def update_menu_item_price(sender, instance, **kwargs):
	instance.menu_item.save()

@receiver(post_save, sender='inventory.Ingredient')
def update_menu_item_using_ingredient(sender, instance, **kwargs):
	for mi in instance.menuitemingredient_set.all():
	    mi.menu_item.save()
