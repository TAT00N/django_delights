# Generated by Django 4.2.6 on 2023-10-18 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_remove_order_menu_item_remove_order_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderMenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.order')),
            ],
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
        migrations.AddField(
            model_name='order',
            name='menu_items',
            field=models.ManyToManyField(through='inventory.OrderMenuItem', to='inventory.menuitem'),
        ),
    ]
