# Generated by Django 5.0.6 on 2024-05-29 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shophouse', '0003_alter_cart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkoutinfo',
            name='cart',
        ),
        migrations.AddField(
            model_name='checkoutinfo',
            name='cart',
            field=models.ManyToManyField(to='shophouse.cart'),
        ),
    ]
