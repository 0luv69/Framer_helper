# Generated by Django 5.0.6 on 2024-05-31 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shophouse', '0005_alter_shippinginfo_checkout_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippinginfo',
            old_name='recived_items',
            new_name='Shipped_items',
        ),
    ]