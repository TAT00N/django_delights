# Generated by Django 4.2.6 on 2023-10-18 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_menuitem_price_per_unit_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Purchase',
            new_name='Order',
        ),
    ]
