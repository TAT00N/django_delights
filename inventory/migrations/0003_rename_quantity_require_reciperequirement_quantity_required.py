# Generated by Django 4.2.6 on 2023-10-15 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_ingredient_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reciperequirement',
            old_name='quantity_require',
            new_name='quantity_required',
        ),
    ]