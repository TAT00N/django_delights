# Generated by Django 4.2.6 on 2023-10-15 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_rename_quantity_require_reciperequirement_quantity_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItemIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_required', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ingredient')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.menuitem')),
            ],
            options={
                'unique_together': {('menu_item', 'ingredient')},
            },
        ),
        migrations.AddField(
            model_name='menuitem',
            name='ingredients',
            field=models.ManyToManyField(through='inventory.MenuItemIngredient', to='inventory.ingredient'),
        ),
    ]