# Generated by Django 5.1.5 on 2025-01-31 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0004_payment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='price',
            new_name='amount',
        ),
    ]
