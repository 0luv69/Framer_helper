# Generated by Django 5.0.6 on 2024-05-31 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shophouse', '0006_rename_recived_items_shippinginfo_shipped_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippinginfo',
            old_name='Shipped_items',
            new_name='recived_items',
        ),
    ]
