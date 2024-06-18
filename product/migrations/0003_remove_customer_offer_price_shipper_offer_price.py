# Generated by Django 5.0 on 2024-05-24 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_customer_offer_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='offer_price',
        ),
        migrations.AddField(
            model_name='shipper',
            name='offer_price',
            field=models.IntegerField(blank=True, default=1000),
        ),
    ]
